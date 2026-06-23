@isTest
private class FileSummaryServiceTest {

    @TestSetup
    static void setup() {
        Account a = new Account(Name = 'Summary Test Acct');
        insert a;

        // A text attachment (valid UTF-8) and a "binary" one labelled as pdf.
        Attachment txt = new Attachment(
            ParentId = a.Id,
            Name = 'notes.txt',
            ContentType = 'text/plain',
            Body = Blob.valueOf('Customer called about a billing error of $120. Resolved, refund issued.')
        );
        Attachment pdf = new Attachment(
            ParentId = a.Id,
            Name = 'report.pdf',
            ContentType = 'application/pdf',
            Body = Blob.valueOf('binary-ish')
        );
        insert new List<Attachment>{ txt, pdf };
    }

    @isTest
    static void testGetAttachments() {
        Account a = [SELECT Id FROM Account LIMIT 1];
        Test.startTest();
        List<Attachment> result = FileSummaryService.getAttachments(a.Id);
        Test.stopTest();
        System.assertEquals(2, result.size(), 'Should return both attachments');
    }

    @isTest
    static void testNoSelection() {
        Test.startTest();
        String empty = FileSummaryService.summarizeAttachments(new List<Id>());
        String nullArg = FileSummaryService.summarizeAttachments(null);
        Test.stopTest();
        System.assert(empty.startsWith('No files'), 'Empty list message');
        System.assert(nullArg.startsWith('No files'), 'Null arg message');
    }

    @isTest
    static void testOnlyBinarySelectedSkips() {
        Attachment pdf = [SELECT Id FROM Attachment WHERE Name = 'report.pdf' LIMIT 1];
        Test.startTest();
        String result = FileSummaryService.summarizeAttachments(new List<Id>{ pdf.Id });
        Test.stopTest();
        // No text files -> short-circuits before any ConnectApi call.
        System.assert(result.contains('text files'), 'Should report no summarizable text files');
        System.assert(result.contains('report.pdf'), 'Should list the skipped file');
    }
}
