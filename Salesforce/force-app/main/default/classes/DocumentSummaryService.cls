/**
 * Backs the documentSummary LWC. Lists an Account's related Files, Attachments
 * and classic Notes, and summarizes a selected subset (max one of each) via the
 * Summarize_Documents prompt template (ConnectApi.EinsteinLLM).
 */
public with sharing class DocumentSummaryService {

    /**
     * Returns the Files (ContentDocument), Attachments and classic Notes related
     * to the given Account, as a flat list for a datatable.
     */
    @AuraEnabled(cacheable=true)
    public static List<DocumentRow> getRelatedDocuments(Id accountId) {
        if (accountId == null) {
            throw new AuraHandledException('An Account Id is required.');
        }

        List<DocumentRow> rows = new List<DocumentRow>();

        try {
            // Files (and exclude notes, which are ContentDocuments with FileType SNOTE)
            for (ContentDocumentLink link : [
                SELECT ContentDocumentId,
                       ContentDocument.Title,
                       ContentDocument.FileType,
                       ContentDocument.ContentSize,
                       ContentDocument.CreatedDate
                FROM ContentDocumentLink
                WHERE LinkedEntityId = :accountId
                AND ContentDocument.FileType != 'SNOTE'
                WITH USER_MODE
            ]) {
                DocumentRow row = new DocumentRow();
                row.id = link.ContentDocumentId;
                row.name = link.ContentDocument.Title;
                row.type = 'File';
                row.docType = link.ContentDocument.FileType;
                row.createdDate = link.ContentDocument.CreatedDate;
                rows.add(row);
            }

            // Classic Notes
            for (Note n : [
                SELECT Id, Title, CreatedDate
                FROM Note
                WHERE ParentId = :accountId
                WITH USER_MODE
            ]) {
                DocumentRow row = new DocumentRow();
                row.id = n.Id;
                row.name = n.Title;
                row.type = 'Note';
                row.docType = 'Note';
                row.createdDate = n.CreatedDate;
                rows.add(row);
            }

            // Attachments
            for (Attachment a : [
                SELECT Id, Name, ContentType, CreatedDate
                FROM Attachment
                WHERE ParentId = :accountId
                WITH USER_MODE
            ]) {
                DocumentRow row = new DocumentRow();
                row.id = a.Id;
                row.name = a.Name;
                row.type = 'Attachment';
                row.docType = a.ContentType;
                row.createdDate = a.CreatedDate;
                rows.add(row);
            }
        } catch (Exception e) {
            throw new AuraHandledException('Unable to load related documents: ' + e.getMessage());
        }

        return rows;
    }

    /**
     * Summarizes any combination (at most one each) of a File, Attachment and Note
     * by invoking the Summarize_Documents prompt template. Returns an HTML fragment
     * containing a section per provided source.
     */
    @AuraEnabled(cacheable=false)
    public static String summarizeDocuments(Id fileId, Id attachmentId, Id noteId) {
        if (fileId == null && attachmentId == null && noteId == null) {
            throw new AuraHandledException('Select at least one document to summarize.');
        }

        // Only pass the inputs the user actually selected; all template inputs are optional.
        // Files and Attachments are passed as extracted text (the platform's merge fields
        // surface only the record Id, not the document body); the Note is passed as a record
        // so the template can merge its Title/Body fields directly.
        Map<String, ConnectApi.WrappedValue> inputParams = new Map<String, ConnectApi.WrappedValue>();

        if (fileId != null) {
            String fileText = getFileText(fileId);
            if (String.isNotBlank(fileText)) {
                inputParams.put('Input:File_Content', wrapString(fileText));
            }
        }
        if (attachmentId != null) {
            String attachmentText = getAttachmentText(attachmentId);
            if (String.isNotBlank(attachmentText)) {
                inputParams.put('Input:Attachment_Content', wrapString(attachmentText));
            }
        }
        if (noteId != null) {
            inputParams.put('Input:Note', wrapRecord(noteId));
        }

        if (inputParams.isEmpty()) {
            throw new AuraHandledException('No readable text could be extracted from the selected document(s). Binary files (e.g. PDF, Word, images) are not supported for text summarization.');
        }

        try {
            ConnectApi.EinsteinPromptTemplateGenerationsInput input =
                new ConnectApi.EinsteinPromptTemplateGenerationsInput();
            input.additionalConfig = new ConnectApi.EinsteinLlmAdditionalConfigInput();
            input.additionalConfig.applicationName = 'PromptBuilderPreview';
            input.isPreview = false;
            input.inputParams = inputParams;

            ConnectApi.EinsteinPromptTemplateGenerationsRepresentation output =
                ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate('Summarize_Documents', input);

            if (output == null || output.generations == null || output.generations.isEmpty()) {
                throw new AuraHandledException('The summary service returned no result.');
            }
            return output.generations[0].text;
        } catch (AuraHandledException e) {
            throw e;
        } catch (Exception e) {
            throw new AuraHandledException('Summary generation failed: ' + e.getMessage());
        }
    }

    // Wraps a record Id in the {'id' => recordId} shape the prompt template expects for object inputs.
    private static ConnectApi.WrappedValue wrapRecord(Id recordId) {
        ConnectApi.WrappedValue wrapped = new ConnectApi.WrappedValue();
        wrapped.value = new Map<String, String>{ 'id' => recordId };
        return wrapped;
    }

    // Wraps a plain string for a primitive String template input.
    private static ConnectApi.WrappedValue wrapString(String value) {
        ConnectApi.WrappedValue wrapped = new ConnectApi.WrappedValue();
        wrapped.value = value;
        return wrapped;
    }

    private static final Integer MAX_TEXT_LENGTH = 100000;

    // Reads the latest ContentVersion body for a File and returns it as text, or null
    // when the file is binary / cannot be decoded as text.
    private static String getFileText(Id contentDocumentId) {
        List<ContentVersion> versions = [
            SELECT VersionData
            FROM ContentVersion
            WHERE ContentDocumentId = :contentDocumentId
            AND IsLatest = true
            WITH USER_MODE
            LIMIT 1
        ];
        if (versions.isEmpty()) {
            return null;
        }
        return blobToText(versions[0].VersionData);
    }

    // Reads an Attachment body and returns it as text, or null when it is binary.
    private static String getAttachmentText(Id attachmentId) {
        List<Attachment> attachments = [
            SELECT Body
            FROM Attachment
            WHERE Id = :attachmentId
            WITH USER_MODE
            LIMIT 1
        ];
        if (attachments.isEmpty()) {
            return null;
        }
        return blobToText(attachments[0].Body);
    }

    // Decodes a Blob to text, capping length to protect the heap and the prompt size.
    // Returns null if the content cannot be decoded (e.g. genuinely binary data).
    private static String blobToText(Blob data) {
        if (data == null) {
            return null;
        }
        try {
            String text = data.toString();
            if (text != null && text.length() > MAX_TEXT_LENGTH) {
                text = text.substring(0, MAX_TEXT_LENGTH);
            }
            return text;
        } catch (Exception e) {
            return null;
        }
    }

    public class DocumentRow {
        @AuraEnabled public String id;
        @AuraEnabled public String name;
        @AuraEnabled public String type;       // File | Attachment | Note
        @AuraEnabled public String docType;    // FileType / ContentType / 'Note'
        @AuraEnabled public Datetime createdDate;
    }
}
