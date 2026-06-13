import { LightningElement, api, wire } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import getRelatedDocuments from '@salesforce/apex/DocumentSummaryService.getRelatedDocuments';
import summarizeDocuments from '@salesforce/apex/DocumentSummaryService.summarizeDocuments';

const COLUMNS = [
    { label: 'Name', fieldName: 'name', type: 'text', wrapText: true },
    { label: 'Type', fieldName: 'type', type: 'text', fixedWidth: 120 },
    {
        label: 'Created',
        fieldName: 'createdDate',
        type: 'date',
        typeAttributes: {
            year: 'numeric',
            month: 'short',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        }
    }
];

export default class DocumentSummary extends LightningElement {
    // recordId is populated automatically on a record page; accountId is the
    // App/Home page fallback property.
    @api recordId;
    @api accountId;

    columns = COLUMNS;
    rows = [];
    loadError;

    // Controlled selection: array of row ids (the datatable key-field).
    selectedRows = [];
    selectedFileId = null;
    selectedAttachmentId = null;
    selectedNoteId = null;

    summary;
    errorMessage;
    isLoading = false;

    get effectiveAccountId() {
        return this.accountId || this.recordId;
    }

    @wire(getRelatedDocuments, { accountId: '$effectiveAccountId' })
    wiredDocs({ error, data }) {
        if (data) {
            this.rows = data;
            this.loadError = undefined;
        } else if (error) {
            this.rows = [];
            this.loadError = this.reduceError(error);
        }
    }

    get hasRows() {
        return this.rows && this.rows.length > 0;
    }

    get hasSelection() {
        return Boolean(this.selectedFileId || this.selectedAttachmentId || this.selectedNoteId);
    }

    get isSummarizeDisabled() {
        return this.isLoading || !this.hasSelection;
    }

    get hasSummary() {
        return this.summary && this.summary.length > 0;
    }

    get hasError() {
        return this.errorMessage && this.errorMessage.length > 0;
    }

    // Enforce at most one selected row per type. If the user picks a second row of
    // a type already selected, the newest pick replaces the previous one.
    handleRowSelection(event) {
        const selected = event.detail.selectedRows || [];
        const previousIds = new Set(this.selectedRows);

        const byType = { File: [], Attachment: [], Note: [] };
        selected.forEach((row) => {
            if (byType[row.type]) {
                byType[row.type].push(row);
            }
        });

        const kept = [];
        let replaced = false;
        Object.keys(byType).forEach((type) => {
            const group = byType[type];
            if (group.length === 0) {
                return;
            }
            if (group.length === 1) {
                kept.push(group[0]);
                return;
            }
            // More than one of this type: keep the newly added row (fall back to last).
            const newlyAdded = group.filter((row) => !previousIds.has(row.id));
            kept.push(newlyAdded.length ? newlyAdded[newlyAdded.length - 1] : group[group.length - 1]);
            replaced = true;
        });

        this.selectedRows = kept.map((row) => row.id);
        this.selectedFileId = this.idForType(kept, 'File');
        this.selectedAttachmentId = this.idForType(kept, 'Attachment');
        this.selectedNoteId = this.idForType(kept, 'Note');

        if (replaced) {
            this.showToast('Selection updated', 'You can select only one item per type.', 'info');
        }
    }

    idForType(rows, type) {
        const match = rows.find((row) => row.type === type);
        return match ? match.id : null;
    }

    handleSummarize() {
        if (!this.hasSelection) {
            this.showToast('Error', 'Select at least one document to summarize.', 'error');
            return;
        }
        this.isLoading = true;
        this.errorMessage = '';
        this.summary = '';
        summarizeDocuments({
            fileId: this.selectedFileId,
            attachmentId: this.selectedAttachmentId,
            noteId: this.selectedNoteId
        })
            .then((result) => {
                this.summary = result;
                this.showToast('Success', 'Summary generated.', 'success');
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
        this.selectedRows = [];
        this.selectedFileId = null;
        this.selectedAttachmentId = null;
        this.selectedNoteId = null;
    }

    reduceError(error) {
        if (Array.isArray(error.body)) {
            return error.body.map((e) => e.message).join(', ');
        } else if (error.body && typeof error.body.message === 'string') {
            return error.body.message;
        }
        return 'Unknown error';
    }

    showToast(title, message, variant) {
        this.dispatchEvent(new ShowToastEvent({ title, message, variant }));
    }
}
