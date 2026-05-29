# Document Translation Workflow SOP — CAG Platform

## Overview
This SOP defines the end-to-end process for uploading, translating, vetting, formatting, compiling, and dispatching documents on the CAG platform. The workflow involves Office Admins, End Users, and the Bhashini translation engine.

---

## Section 1: Supported Document Types and Limits

### 1.1 Accepted File Formats
- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Plain Text (.txt)
- OpenDocument Text (.odt)

### 1.2 File Size and Page Limits
- Maximum file size per upload: **10 MB**
- Maximum pages per document: **100 pages**
- Maximum documents per batch upload: **20 files**

### 1.3 Supported Languages
The platform supports translation between English and the following Indian languages:
Hindi (hi), Bengali (bn), Telugu (te), Marathi (mr), Tamil (ta), Gujarati (gu), Kannada (kn), Malayalam (ml), Punjabi (pa), Odia (or), Urdu (ur), and Assamese (as).

---

## Section 2: Document Upload

### 2.1 Who Can Upload
- Office Admins can upload documents on behalf of their office.
- End Users can upload documents if the Office Admin has granted upload permission.

### 2.2 Steps to Upload a Document
1. Log in as Office Admin (or End User with upload permission).
2. Navigate to **Document Management → Upload Document**.
3. Click **Choose File** and select the document from your device.
4. Fill in the **Document Metadata** form:
   - Document Title (mandatory)
   - Source Language (the language the document is currently in)
   - Target Language(s) (one or more languages to translate into)
   - Category (e.g., Circular, Notification, Report, Form)
   - Priority Level: Normal / Urgent
5. Click **Upload**. The system validates the file format and size.
6. Upon successful validation, the document appears in the **Pending Translation** queue with status **Uploaded**.

### 2.3 Bulk Upload
1. Navigate to **Document Management → Bulk Upload**.
2. Click **Download CSV Template** and fill in metadata for each file.
3. Zip the document files together with the completed CSV.
4. Upload the zip file.
5. The system processes each document individually and displays a summary.

---

## Section 3: Translation Process

### 3.1 Automatic Translation via Bhashini API
1. Once a document is in the **Pending Translation** queue, the system automatically submits it to the Bhashini Dhruva pipeline.
2. The translation engine processes the document and returns the translated text.
3. The document status changes to **Translation Complete — Pending Review**.
4. If the Bhashini API is unavailable, the system retries up to 3 times with a 5-minute interval, then escalates to **Manual Translation Required** status.

### 3.2 Translation Status Codes
| Status | Meaning |
|--------|---------|
| Uploaded | Document received, not yet submitted for translation |
| In Translation | Submitted to Bhashini, awaiting result |
| Translation Complete — Pending Review | Translated, awaiting vetting |
| Under Review | A reviewer is actively vetting the translation |
| Approved | Translation accepted, ready for formatting |
| Rejected | Translation failed review, returned for re-translation |
| Manual Translation Required | Auto-translation failed, human translator needed |
| Formatted | Post-translation formatting complete |
| Compiled | Part of a compiled document set |
| Dispatched | Sent to end users/stakeholders |

---

## Section 4: Vetting (Review)

### 4.1 Who Reviews Translations
- Super Admins or designated Language Reviewers vet translated documents.
- Office Admins can review documents within their office scope.

### 4.2 Steps for Vetting
1. Reviewer logs in and navigates to **Translation Queue → Pending Review**.
2. Selects a document to review. The system opens a side-by-side view: source on the left, translation on the right.
3. Reviewer reads through the translation and can:
   - **Edit** inline text corrections directly in the translation panel.
   - **Add Comments** on specific paragraphs or sentences using the comment tool.
   - **Highlight** problematic sections.
4. After review, reviewer selects one of:
   - **Approve** — marks translation as approved.
   - **Reject with Reason** — sends the document back for re-translation with comments attached.
5. The document status updates accordingly and the Office Admin is notified.

### 4.3 Re-translation After Rejection
1. Office Admin receives notification that the document was rejected.
2. Office Admin can click **Request Re-translation** from the document detail page.
3. The system resubmits the document to Bhashini with the reviewer's comments passed as context notes.
4. The new translation enters the review queue again.

---

## Section 5: Formatting

### 5.1 Purpose
Formatting ensures translated documents retain the original layout — headings, bullet points, tables, and page structure — after translation.

### 5.2 Steps for Formatting
1. Once a document is **Approved**, it moves to the **Pending Formatting** queue.
2. An Office Admin or designated Formatter opens the document in **Formatting Tools**.
3. Available formatting actions:
   - Apply document template (letterhead, government format, plain).
   - Adjust font to Unicode-compatible font for the target language (e.g., Noto Sans for Devanagari).
   - Rebuild tables and lists that may have shifted during translation.
   - Insert header/footer with document metadata (title, date, reference number).
4. Click **Save Formatted Version**.
5. Document status changes to **Formatted**.

### 5.3 Automated Formatting
If **Auto-Format** is enabled in office settings:
- The system applies the default template automatically after approval.
- The Office Admin still receives a notification to review the auto-formatted version before dispatch.

---

## Section 6: Compilation

### 6.1 Purpose
Compilation groups multiple related translated documents into a single package (e.g., a quarterly report set, a policy bundle).

### 6.2 Steps to Compile Documents
1. Navigate to **Document Management → Compile**.
2. Click **New Compilation**.
3. Give the compilation a title and description.
4. From the **Formatted Documents** list, select the documents to include.
5. Drag to reorder documents within the compilation.
6. Click **Compile**. The system generates a merged PDF or zip file.
7. The compiled package appears in **My Compilations** with status **Compiled**.

### 6.3 Compilation Rules
- Only documents with status **Formatted** or **Approved** can be compiled.
- A document can be part of multiple compilations.
- Maximum 50 documents per compilation.

---

## Section 7: Dispatch

### 7.1 Who Can Dispatch
Office Admins can dispatch documents or compiled packages to End Users and external stakeholders.

### 7.2 Dispatch to End Users
1. Navigate to **Document Management → Dispatch**.
2. Select the document(s) or compiled package to dispatch.
3. In **Recipient Selection**, choose one of:
   - Individual End Users (search by name or email).
   - User Group (all End Users in the office, or a custom group).
4. Add an optional cover message.
5. Choose delivery method: **In-Platform Notification** or **Email Attachment** (or both).
6. Click **Dispatch**. All selected recipients receive the document.
7. Document status updates to **Dispatched**. A dispatch log entry is created.

### 7.3 Dispatch to External Stakeholders
1. Follow the same steps as above.
2. In **Recipient Selection**, switch to the **External** tab.
3. Enter the external email address(es) manually or import from CSV.
4. Click **Dispatch**. The system sends the document as an email attachment with a secure download link.

### 7.4 Dispatch Logs and Tracking
- All dispatches are logged under **Audit → Dispatch History**.
- Log entries include: Document title, recipients, dispatch timestamp, delivery status (Sent / Opened / Failed).
- Office Admins can resend failed dispatches from the dispatch log.

---

## Section 8: Common Issues and Resolutions

### 8.1 Upload Fails — File Too Large
- Check that the file is under 10 MB.
- Compress the PDF using a PDF optimiser tool before re-uploading.
- Split large documents into multiple uploads if they exceed 100 pages.

### 8.2 Upload Fails — Unsupported Format
- Convert the file to PDF or DOCX before uploading.
- Scanned PDFs must be OCR-processed before uploading; the platform does not currently perform OCR.

### 8.3 Translation Taking Too Long
- Normal translation time is 2–10 minutes depending on document length.
- If status stays as **In Translation** for more than 30 minutes, click **Retry Translation** on the document detail page.
- If retrying does not help, the document will be escalated to **Manual Translation Required**.

### 8.4 Translation Quality Issues
- Use the Vetting step to correct errors rather than re-uploading the document.
- For systematic quality issues, report to the Super Admin who can adjust Bhashini model settings.

### 8.5 Formatting Breaks After Translation
- This is common with complex tables and multi-column layouts.
- Use **Formatting Tools → Manual Format** to rebuild affected sections.
- Switch to a simpler source template (plain text or single-column) for better results.

### 8.6 Dispatch Delivery Failure
- Check the recipient's email address for typos.
- If the email bounced, navigate to **Dispatch History → Resend**.
- In-platform notifications require the recipient to have an active account and notifications enabled.

---

## Section 9: Document Retention Policy

- All uploaded and translated documents are retained for **5 years** from the dispatch date.
- After 5 years, documents are archived and not accessible through the platform UI.
- To request access to archived documents, submit a request to the Super Admin.
- Deleted accounts' documents are retained but anonymised for the full retention period.
