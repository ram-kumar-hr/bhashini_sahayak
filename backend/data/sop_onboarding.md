# Onboarding Workflow SOP — CAG Platform

## Overview
This SOP defines how users at every role level are invited, registered, and assigned roles on the CAG (Common Assistance Group) platform. There are four role tiers: CEO, Super Admin, Office Admin, and End User.

---

## Section 1: CEO Onboarding

### 1.1 Who Can Onboard a CEO
Only the Platform Super Administrator (system-level) can create a CEO account. This is typically performed once during initial platform deployment.

### 1.2 Steps to Onboard a CEO
1. Log in to the platform as Platform Super Administrator.
2. Navigate to **Admin Panel → User Management → Create CEO**.
3. Enter the CEO's full name, official email address, and organisation name.
4. Assign the **CEO** role from the role dropdown.
5. Click **Send Invitation**. The system sends an invitation email with a one-time setup link valid for 48 hours.
6. The CEO clicks the link, sets a password, and completes two-factor authentication (2FA) setup.
7. Upon successful 2FA registration, the CEO account is activated.

### 1.3 CEO Permissions
- Create and manage Super Admin accounts.
- View organisation-wide analytics and reports.
- Configure global platform settings.
- Cannot directly process documents or translation tasks.

---

## Section 2: Super Admin Onboarding

### 2.1 Who Can Onboard a Super Admin
A CEO or Platform Super Administrator can create Super Admin accounts.

### 2.2 Steps to Onboard a Super Admin
1. Log in as CEO.
2. Go to **Admin Panel → User Management → Create Super Admin**.
3. Fill in: Full Name, Email, Phone Number, Assigned Region/State.
4. Select **Super Admin** from the role dropdown.
5. Click **Send Invitation**. An email is dispatched with a setup link (valid 48 hours).
6. The Super Admin follows the link, creates a password, and activates their account.
7. CEO must then assign the Super Admin to one or more **Office Groups** from the **Office Management** menu.

### 2.3 Super Admin Permissions
- Create and manage Office Admin accounts within their assigned region.
- View region-level reports and translation queues.
- Approve or reject escalated translation tasks.
- Cannot directly upload or translate documents.

---

## Section 3: Office Admin Onboarding

### 3.1 Who Can Onboard an Office Admin
A Super Admin or CEO can create Office Admin accounts.

### 3.2 Steps to Onboard an Office Admin
1. Log in as Super Admin.
2. Navigate to **Office Management → Select Office → Add Office Admin**.
3. Enter: Full Name, Email, Phone, Designation.
4. Assign the **Office Admin** role and select the specific office from the office list.
5. Click **Invite**. The system sends an invitation email valid for 72 hours.
6. Office Admin clicks the invitation link, sets a password, and logs in.
7. Super Admin must confirm the Office Admin is linked to the correct office in **Office Management → Office Admin List**.

### 3.3 Office Admin Permissions
- Add and manage End Users within their office.
- Upload documents for translation.
- Monitor translation status for their office.
- Assign translation tasks to End Users.
- Cannot create other Office Admins or Super Admins.

---

## Section 4: End User Onboarding

### 4.1 Who Can Onboard an End User
Office Admins can onboard End Users. End Users may also self-register if the platform has self-registration enabled.

### 4.2 Steps for Office Admin-Initiated Onboarding
1. Log in as Office Admin.
2. Go to **User Management → Add End User**.
3. Enter: Full Name, Email, Phone Number, Preferred Language.
4. Click **Send Invite**. The End User receives an email with a registration link (valid 24 hours).
5. End User clicks the link, fills in profile details, sets a password, and submits.
6. Office Admin receives a notification and approves the registration from **Pending Approvals**.
7. End User account is activated upon approval.

### 4.3 Steps for Self-Registration (if enabled)
1. End User visits the CAG platform login page and clicks **Register**.
2. Fills in full name, email, phone, office code (provided by their Office Admin), and preferred language.
3. Submits the form. A verification email is sent to their address.
4. End User verifies email by clicking the link.
5. Office Admin is notified and approves the registration.
6. End User receives confirmation and can now log in.

### 4.4 End User Permissions
- View and download assigned translated documents.
- Submit queries through the help desk.
- Update their own profile and language preferences.
- Cannot access admin panels or create other user accounts.

---

## Section 5: Role Summary Table

| Role         | Created By             | Can Create          | Key Access                          |
|--------------|------------------------|---------------------|-------------------------------------|
| CEO          | Platform Super Admin   | Super Admin         | Organisation-wide management        |
| Super Admin  | CEO                    | Office Admin        | Region/state-level management       |
| Office Admin | Super Admin or CEO     | End User            | Office-level document management    |
| End User     | Office Admin (or self) | None                | Document access, query submission   |

---

## Section 6: Common Onboarding Issues and Resolutions

### 6.1 Invitation Email Not Received
- Ask the user to check their spam/junk folder.
- Verify the email address entered was correct in the admin panel.
- Office Admin or Super Admin can resend the invitation from **User Management → Pending Invitations → Resend**.
- Invitation links expire: CEO/Super Admin links after 48 hours, Office Admin links after 72 hours, End User links after 24 hours.

### 6.2 Invitation Link Expired
- The inviting admin navigates to **User Management → Pending Invitations**.
- Finds the user record and clicks **Resend Invitation**.
- A fresh link is generated and emailed.

### 6.3 User Cannot Set Password
- Password must be at least 8 characters, contain one uppercase letter, one number, and one special character.
- If the form gives an error, ensure browser autofill is not inserting incorrect characters.
- User can click **Forgot Password** on the login page to trigger a reset email.

### 6.4 2FA Setup Issues (CEO only)
- CEO must download an authenticator app (Google Authenticator or Microsoft Authenticator).
- Scan the QR code displayed on the 2FA setup screen.
- Enter the 6-digit code shown in the app within 30 seconds.
- If the code is rejected, ensure device time is synced (NTP).

### 6.5 Wrong Role Assigned
- A user's role can be changed by their direct creator (e.g., CEO can change a Super Admin's role).
- Navigate to **User Management → Find User → Edit → Change Role**.
- Save changes. The user must log out and back in for the new role to take effect.

---

## Section 7: Deactivating and Removing Accounts

### 7.1 Deactivating an Account
- Deactivated accounts cannot log in but data is preserved.
- Navigate to **User Management → Find User → Deactivate**.
- Confirm the action. The user receives an email notification.

### 7.2 Permanently Removing an Account
- Only CEOs can permanently delete Super Admin or Office Admin accounts.
- Office Admins can delete End User accounts in their office.
- Navigate to **User Management → Find User → Delete Account**.
- Type the user's email to confirm deletion.
- All data associated with that user is anonymised, not deleted, for audit purposes.
