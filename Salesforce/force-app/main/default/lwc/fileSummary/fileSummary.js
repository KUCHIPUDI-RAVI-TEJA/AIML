import { LightningElement, api, wire } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import getAttachments from '@salesforce/apex/FileSummaryService.getAttachments';
import summarizeAttachments from '@salesforce/apex/FileSummaryService.summarizeAttachments';

const COLUMNS = [
    { label: 'File Name', fieldName: 'Name', type: 'text' },
    { label: 'Type', fieldName: 'ContentType', type: 'text' },
    { label: 'Size (bytes)', fieldName: 'BodyLength', type: 'number' }
];

export default class FileSummary extends LightningElement {
    @api recordId;

    columns = COLUMNS;
    attachments = [];
    selectedIds = [];
    isLoading = false;
    summary;
    errorMessage;

    @wire(getAttachments, { recordId: '$recordId' })
    wiredAttachments({ data, error }) {
        if (data) {
            this.attachments = data;
            this.errorMessage = '';
        } else if (error) {
            this.errorMessage = this.reduceError(error);
        }
    }

    handleRowSelection(event) {
        this.selectedIds = event.detail.selectedRows.map((row) => row.Id);
    }

    handleSummarize() {
        if (!this.selectedIds.length) {
            this.errorMessage = 'Please select at least one file to summarize.';
            this.showToast('Error', this.errorMessage, 'error');
            return;
        }

        this.isLoading = true;
        this.errorMessage = '';
        this.summary = '';

        summarizeAttachments({ attachmentIds: this.selectedIds })
            .then((result) => {
                this.summary = result;
                this.showToast('Success', 'Summary generated', 'success');
            })
            .catch((error) => {
                this.errorMessage = this.reduceError(error);
                this.showToast('Error', this.errorMessage, 'error');
            })
            .finally(() => {
                this.isLoading = false;
            });
    }

    handleClear() {
        this.summary = '';
        this.errorMessage = '';
        this.selectedIds = [];
        const table = this.template.querySelector('lightning-datatable');
        if (table) {
            table.selectedRows = [];
        }
    }

    showToast(title, message, variant) {
        this.dispatchEvent(new ShowToastEvent({ title, message, variant }));
    }

    reduceError(error) {
        if (error && error.body && error.body.message) {
            return error.body.message;
        }
        return 'An unexpected error occurred.';
    }

    get hasAttachments() {
        return this.attachments && this.attachments.length > 0;
    }

    get hasSummary() {
        return this.summary && this.summary.length > 0;
    }

    get hasError() {
        return this.errorMessage && this.errorMessage.length > 0;
    }

    get isSummarizeDisabled() {
        return this.isLoading || !this.selectedIds.length;
    }
}
