public with sharing class FileSummaryService {

    // Developer name of the Flex prompt template that takes a single String input (File_Text)
    private static final String TEMPLATE_DEV_NAME = 'Summarize_File_Text';

    /**
     * Returns the Attachments belonging to a record so the LWC can list them for selection.
     * Body is intentionally not queried here (no need to ship blobs to the client).
     */
    @AuraEnabled(cacheable=true)
    public static List<Attachment> getAttachments(Id recordId) {
        return [
            SELECT Id, Name, ContentType, BodyLength
            FROM Attachment
            WHERE ParentId = :recordId
            ORDER BY CreatedDate DESC
        ];
    }

    /**
     * Decodes the body of each selected text Attachment and asks the prompt template
     * to summarize the combined content. Non-text/binary files are skipped (deferred scope).
     */
    @AuraEnabled(cacheable=false)
    public static String summarizeAttachments(List<Id> attachmentIds) {
        if (attachmentIds == null || attachmentIds.isEmpty()) {
            return 'No files were selected.';
        }

        List<Attachment> atts = [
            SELECT Id, Name, ContentType, Body
            FROM Attachment
            WHERE Id IN :attachmentIds
        ];

        List<String> textBlocks = new List<String>();
        List<String> skipped = new List<String>();

        for (Attachment a : atts) {
            String txt = tryDecodeText(a);
            if (txt != null) {
                textBlocks.add('### ' + a.Name + '\n' + txt);
            } else {
                skipped.add(a.Name);
            }
        }

        if (textBlocks.isEmpty()) {
            return 'None of the selected files are text files that can be summarized yet. '
                 + 'Skipped: ' + String.join(skipped, ', ');
        }

        String combined = String.join(textBlocks, '\n\n');
        String summary = callPromptTemplate(combined);

        if (!skipped.isEmpty()) {
            summary += '<p><i>Note: skipped non-text files: '
                     + String.escapeSingleQuotes(String.join(skipped, ', ')) + '</i></p>';
        }
        return summary;
    }

    /**
     * Returns the decoded text for text-based attachments, or null if the file is
     * binary / cannot be decoded as UTF-8.
     */
    private static String tryDecodeText(Attachment a) {
        Boolean looksText = (a.ContentType != null && a.ContentType.startsWith('text/'))
            || (a.Name != null && (a.Name.endsWithIgnoreCase('.txt') || a.Name.endsWithIgnoreCase('.csv')));
        if (!looksText) {
            return null;
        }
        if (a.Body == null) {
            return null;
        }
        try {
            return a.Body.toString(); // UTF-8 decode (verified valid for our files)
        } catch (Exception e) {
            // Not valid UTF-8 (e.g. a binary file mislabeled as text) — skip it.
            return null;
        }
    }

    /**
     * Invokes the Flex prompt template, passing the file text as the String input.
     * Mirrors the working pattern in FileQnAService (template devName is the first arg).
     */
    private static String callPromptTemplate(String fileText) {
        ConnectApi.WrappedValue fileTextValue = new ConnectApi.WrappedValue();
        fileTextValue.value = fileText;

        Map<String, ConnectApi.WrappedValue> inputParams =
            new Map<String, ConnectApi.WrappedValue>();
        inputParams.put('Input:File_Text', fileTextValue);

        ConnectApi.EinsteinPromptTemplateGenerationsInput templateInput =
            new ConnectApi.EinsteinPromptTemplateGenerationsInput();
        templateInput.additionalConfig = new ConnectApi.EinsteinLlmAdditionalConfigInput();
        templateInput.additionalConfig.applicationName = 'PromptBuilderPreview';
        templateInput.isPreview = false;
        templateInput.inputParams = inputParams;

        ConnectApi.EinsteinPromptTemplateGenerationsRepresentation output =
            ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(
                TEMPLATE_DEV_NAME, templateInput);

        return output.generations[0].text;
    }
}
