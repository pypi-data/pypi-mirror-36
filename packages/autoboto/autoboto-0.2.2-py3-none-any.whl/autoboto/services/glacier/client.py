import datetime
import typing
import boto3
from autoboto import ShapeBase, OutputShapeBase
from . import shapes


class Client:
    def __init__(self, *args, **kwargs):
        self._boto_client = boto3.client("glacier", *args, **kwargs)

    def abort_multipart_upload(
        self,
        _request: shapes.AbortMultipartUploadInput = None,
        *,
        account_id: str,
        vault_name: str,
        upload_id: str,
    ) -> None:
        """
        This operation aborts a multipart upload identified by the upload ID.

        After the Abort Multipart Upload request succeeds, you cannot upload any more
        parts to the multipart upload or complete the multipart upload. Aborting a
        completed upload fails. However, aborting an already-aborted upload will
        succeed, for a short time. For more information about uploading a part and
        completing a multipart upload, see UploadMultipartPart and
        CompleteMultipartUpload.

        This operation is idempotent.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Working with Archives
        in Amazon Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/working-
        with-archives.html) and [Abort Multipart
        Upload](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-multipart-abort-
        upload.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if upload_id is not ShapeBase.NOT_SET:
                _params['upload_id'] = upload_id
            _request = shapes.AbortMultipartUploadInput(**_params)
        response = self._boto_client.abort_multipart_upload(
            **_request.to_boto_dict()
        )

    def abort_vault_lock(
        self,
        _request: shapes.AbortVaultLockInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> None:
        """
        This operation aborts the vault locking process if the vault lock is not in the
        `Locked` state. If the vault lock is in the `Locked` state when this operation
        is requested, the operation returns an `AccessDeniedException` error. Aborting
        the vault locking process removes the vault lock policy from the specified
        vault.

        A vault lock is put into the `InProgress` state by calling InitiateVaultLock. A
        vault lock is put into the `Locked` state by calling CompleteVaultLock. You can
        get the state of a vault lock by calling GetVaultLock. For more information
        about the vault locking process, see [Amazon Glacier Vault
        Lock](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-lock.html). For
        more information about vault lock policies, see [Amazon Glacier Access Control
        with Vault Lock
        Policies](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-lock-
        policy.html).

        This operation is idempotent. You can successfully invoke this operation
        multiple times, if the vault lock is in the `InProgress` state or if there is no
        policy associated with the vault.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.AbortVaultLockInput(**_params)
        response = self._boto_client.abort_vault_lock(**_request.to_boto_dict())

    def add_tags_to_vault(
        self,
        _request: shapes.AddTagsToVaultInput = None,
        *,
        account_id: str,
        vault_name: str,
        tags: typing.Dict[str, str] = ShapeBase.NOT_SET,
    ) -> None:
        """
        This operation adds the specified tags to a vault. Each tag is composed of a key
        and a value. Each vault can have up to 10 tags. If your request would cause the
        tag limit for the vault to be exceeded, the operation throws the
        `LimitExceededException` error. If a tag already exists on the vault under a
        specified key, the existing key value will be overwritten. For more information
        about tags, see [Tagging Amazon Glacier
        Resources](http://docs.aws.amazon.com/amazonglacier/latest/dev/tagging.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if tags is not ShapeBase.NOT_SET:
                _params['tags'] = tags
            _request = shapes.AddTagsToVaultInput(**_params)
        response = self._boto_client.add_tags_to_vault(
            **_request.to_boto_dict()
        )

    def complete_multipart_upload(
        self,
        _request: shapes.CompleteMultipartUploadInput = None,
        *,
        account_id: str,
        vault_name: str,
        upload_id: str,
        archive_size: str = ShapeBase.NOT_SET,
        checksum: str = ShapeBase.NOT_SET,
    ) -> shapes.ArchiveCreationOutput:
        """
        You call this operation to inform Amazon Glacier that all the archive parts have
        been uploaded and that Amazon Glacier can now assemble the archive from the
        uploaded parts. After assembling and saving the archive to the vault, Amazon
        Glacier returns the URI path of the newly created archive resource. Using the
        URI path, you can then access the archive. After you upload an archive, you
        should save the archive ID returned to retrieve the archive at a later point.
        You can also get the vault inventory to obtain a list of archive IDs in a vault.
        For more information, see InitiateJob.

        In the request, you must include the computed SHA256 tree hash of the entire
        archive you have uploaded. For information about computing a SHA256 tree hash,
        see [Computing
        Checksums](http://docs.aws.amazon.com/amazonglacier/latest/dev/checksum-
        calculations.html). On the server side, Amazon Glacier also constructs the
        SHA256 tree hash of the assembled archive. If the values match, Amazon Glacier
        saves the archive to the vault; otherwise, it returns an error, and the
        operation fails. The ListParts operation returns a list of parts uploaded for a
        specific multipart upload. It includes checksum information for each uploaded
        part that can be used to debug a bad checksum issue.

        Additionally, Amazon Glacier also checks for any missing content ranges when
        assembling the archive, if missing content ranges are found, Amazon Glacier
        returns an error and the operation fails.

        Complete Multipart Upload is an idempotent operation. After your first
        successful complete multipart upload, if you call the operation again within a
        short period, the operation will succeed and return the same archive ID. This is
        useful in the event you experience a network issue that causes an aborted
        connection or receive a 500 server error, in which case you can repeat your
        Complete Multipart Upload request and get the same archive ID without creating
        duplicate archives. Note, however, that after the multipart upload completes,
        you cannot call the List Parts operation and the multipart upload will not
        appear in List Multipart Uploads response, even if idempotent complete is
        possible.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Uploading Large
        Archives in Parts (Multipart
        Upload)](http://docs.aws.amazon.com/amazonglacier/latest/dev/uploading-archive-
        mpu.html) and [Complete Multipart
        Upload](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-multipart-
        complete-upload.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if upload_id is not ShapeBase.NOT_SET:
                _params['upload_id'] = upload_id
            if archive_size is not ShapeBase.NOT_SET:
                _params['archive_size'] = archive_size
            if checksum is not ShapeBase.NOT_SET:
                _params['checksum'] = checksum
            _request = shapes.CompleteMultipartUploadInput(**_params)
        response = self._boto_client.complete_multipart_upload(
            **_request.to_boto_dict()
        )

        return shapes.ArchiveCreationOutput.from_boto_dict(response)

    def complete_vault_lock(
        self,
        _request: shapes.CompleteVaultLockInput = None,
        *,
        account_id: str,
        vault_name: str,
        lock_id: str,
    ) -> None:
        """
        This operation completes the vault locking process by transitioning the vault
        lock from the `InProgress` state to the `Locked` state, which causes the vault
        lock policy to become unchangeable. A vault lock is put into the `InProgress`
        state by calling InitiateVaultLock. You can obtain the state of the vault lock
        by calling GetVaultLock. For more information about the vault locking process,
        [Amazon Glacier Vault
        Lock](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-lock.html).

        This operation is idempotent. This request is always successful if the vault
        lock is in the `Locked` state and the provided lock ID matches the lock ID
        originally used to lock the vault.

        If an invalid lock ID is passed in the request when the vault lock is in the
        `Locked` state, the operation returns an `AccessDeniedException` error. If an
        invalid lock ID is passed in the request when the vault lock is in the
        `InProgress` state, the operation throws an `InvalidParameter` error.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if lock_id is not ShapeBase.NOT_SET:
                _params['lock_id'] = lock_id
            _request = shapes.CompleteVaultLockInput(**_params)
        response = self._boto_client.complete_vault_lock(
            **_request.to_boto_dict()
        )

    def create_vault(
        self,
        _request: shapes.CreateVaultInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> shapes.CreateVaultOutput:
        """
        This operation creates a new vault with the specified name. The name of the
        vault must be unique within a region for an AWS account. You can create up to
        1,000 vaults per account. If you need to create more vaults, contact Amazon
        Glacier.

        You must use the following guidelines when naming a vault.

          * Names can be between 1 and 255 characters long.

          * Allowed characters are a-z, A-Z, 0-9, '_' (underscore), '-' (hyphen), and '.' (period).

        This operation is idempotent.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Creating a Vault in
        Amazon Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/creating-
        vaults.html) and [Create Vault
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-vault-put.html) in the
        _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.CreateVaultInput(**_params)
        response = self._boto_client.create_vault(**_request.to_boto_dict())

        return shapes.CreateVaultOutput.from_boto_dict(response)

    def delete_archive(
        self,
        _request: shapes.DeleteArchiveInput = None,
        *,
        account_id: str,
        vault_name: str,
        archive_id: str,
    ) -> None:
        """
        This operation deletes an archive from a vault. Subsequent requests to initiate
        a retrieval of this archive will fail. Archive retrievals that are in progress
        for this archive ID may or may not succeed according to the following scenarios:

          * If the archive retrieval job is actively preparing the data for download when Amazon Glacier receives the delete archive request, the archival retrieval operation might fail.

          * If the archive retrieval job has successfully prepared the archive for download when Amazon Glacier receives the delete archive request, you will be able to download the output.

        This operation is idempotent. Attempting to delete an already-deleted archive
        does not result in an error.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Deleting an Archive in
        Amazon Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/deleting-an-
        archive.html) and [Delete
        Archive](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-archive-
        delete.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if archive_id is not ShapeBase.NOT_SET:
                _params['archive_id'] = archive_id
            _request = shapes.DeleteArchiveInput(**_params)
        response = self._boto_client.delete_archive(**_request.to_boto_dict())

    def delete_vault(
        self,
        _request: shapes.DeleteVaultInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> None:
        """
        This operation deletes a vault. Amazon Glacier will delete a vault only if there
        are no archives in the vault as of the last inventory and there have been no
        writes to the vault since the last inventory. If either of these conditions is
        not satisfied, the vault deletion fails (that is, the vault is not removed) and
        Amazon Glacier returns an error. You can use DescribeVault to return the number
        of archives in a vault, and you can use [Initiate a Job (POST
        jobs)](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-initiate-job-
        post.html) to initiate a new inventory retrieval for a vault. The inventory
        contains the archive IDs you use to delete archives using [Delete Archive
        (DELETE archive)](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-
        archive-delete.html).

        This operation is idempotent.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Deleting a Vault in
        Amazon Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/deleting-
        vaults.html) and [Delete Vault
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-vault-delete.html) in
        the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.DeleteVaultInput(**_params)
        response = self._boto_client.delete_vault(**_request.to_boto_dict())

    def delete_vault_access_policy(
        self,
        _request: shapes.DeleteVaultAccessPolicyInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> None:
        """
        This operation deletes the access policy associated with the specified vault.
        The operation is eventually consistent; that is, it might take some time for
        Amazon Glacier to completely remove the access policy, and you might still see
        the effect of the policy for a short time after you send the delete request.

        This operation is idempotent. You can invoke delete multiple times, even if
        there is no policy associated with the vault. For more information about vault
        access policies, see [Amazon Glacier Access Control with Vault Access
        Policies](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-access-
        policy.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.DeleteVaultAccessPolicyInput(**_params)
        response = self._boto_client.delete_vault_access_policy(
            **_request.to_boto_dict()
        )

    def delete_vault_notifications(
        self,
        _request: shapes.DeleteVaultNotificationsInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> None:
        """
        This operation deletes the notification configuration set for a vault. The
        operation is eventually consistent; that is, it might take some time for Amazon
        Glacier to completely disable the notifications and you might still receive some
        notifications for a short time after you send the delete request.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Configuring Vault
        Notifications in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/configuring-
        notifications.html) and [Delete Vault Notification Configuration
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-vault-notifications-
        delete.html) in the Amazon Glacier Developer Guide.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.DeleteVaultNotificationsInput(**_params)
        response = self._boto_client.delete_vault_notifications(
            **_request.to_boto_dict()
        )

    def describe_job(
        self,
        _request: shapes.DescribeJobInput = None,
        *,
        account_id: str,
        vault_name: str,
        job_id: str,
    ) -> shapes.GlacierJobDescription:
        """
        This operation returns information about a job you previously initiated,
        including the job initiation date, the user who initiated the job, the job
        status code/message and the Amazon SNS topic to notify after Amazon Glacier
        completes the job. For more information about initiating a job, see InitiateJob.

        This operation enables you to check the status of your job. However, it is
        strongly recommended that you set up an Amazon SNS topic and specify it in your
        initiate job request so that Amazon Glacier can notify the topic after it
        completes the job.

        A job ID will not expire for at least 24 hours after Amazon Glacier completes
        the job.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For more information about using this operation, see the documentation for the
        underlying REST API [Describe
        Job](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-describe-job-
        get.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if job_id is not ShapeBase.NOT_SET:
                _params['job_id'] = job_id
            _request = shapes.DescribeJobInput(**_params)
        response = self._boto_client.describe_job(**_request.to_boto_dict())

        return shapes.GlacierJobDescription.from_boto_dict(response)

    def describe_vault(
        self,
        _request: shapes.DescribeVaultInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> shapes.DescribeVaultOutput:
        """
        This operation returns information about a vault, including the vault's Amazon
        Resource Name (ARN), the date the vault was created, the number of archives it
        contains, and the total size of all the archives in the vault. The number of
        archives and their total size are as of the last inventory generation. This
        means that if you add or remove an archive from a vault, and then immediately
        use Describe Vault, the change in contents will not be immediately reflected. If
        you want to retrieve the latest inventory of the vault, use InitiateJob. Amazon
        Glacier generates vault inventories approximately daily. For more information,
        see [Downloading a Vault Inventory in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-
        inventory.html).

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Retrieving Vault
        Metadata in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/retrieving-vault-
        info.html) and [Describe Vault
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-vault-get.html) in the
        _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.DescribeVaultInput(**_params)
        response = self._boto_client.describe_vault(**_request.to_boto_dict())

        return shapes.DescribeVaultOutput.from_boto_dict(response)

    def get_data_retrieval_policy(
        self,
        _request: shapes.GetDataRetrievalPolicyInput = None,
        *,
        account_id: str,
    ) -> shapes.GetDataRetrievalPolicyOutput:
        """
        This operation returns the current data retrieval policy for the account and
        region specified in the GET request. For more information about data retrieval
        policies, see [Amazon Glacier Data Retrieval
        Policies](http://docs.aws.amazon.com/amazonglacier/latest/dev/data-retrieval-
        policy.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            _request = shapes.GetDataRetrievalPolicyInput(**_params)
        response = self._boto_client.get_data_retrieval_policy(
            **_request.to_boto_dict()
        )

        return shapes.GetDataRetrievalPolicyOutput.from_boto_dict(response)

    def get_job_output(
        self,
        _request: shapes.GetJobOutputInput = None,
        *,
        account_id: str,
        vault_name: str,
        job_id: str,
        range: str = ShapeBase.NOT_SET,
    ) -> shapes.GetJobOutputOutput:
        """
        This operation downloads the output of the job you initiated using InitiateJob.
        Depending on the job type you specified when you initiated the job, the output
        will be either the content of an archive or a vault inventory.

        You can download all the job output or download a portion of the output by
        specifying a byte range. In the case of an archive retrieval job, depending on
        the byte range you specify, Amazon Glacier returns the checksum for the portion
        of the data. You can compute the checksum on the client and verify that the
        values match to ensure the portion you downloaded is the correct data.

        A job ID will not expire for at least 24 hours after Amazon Glacier completes
        the job. That a byte range. For both archive and inventory retrieval jobs, you
        should verify the downloaded size against the size returned in the headers from
        the **Get Job Output** response.

        For archive retrieval jobs, you should also verify that the size is what you
        expected. If you download a portion of the output, the expected size is based on
        the range of bytes you specified. For example, if you specify a range of
        `bytes=0-1048575`, you should verify your download size is 1,048,576 bytes. If
        you download an entire archive, the expected size is the size of the archive
        when you uploaded it to Amazon Glacier The expected size is also returned in the
        headers from the **Get Job Output** response.

        In the case of an archive retrieval job, depending on the byte range you
        specify, Amazon Glacier returns the checksum for the portion of the data. To
        ensure the portion you downloaded is the correct data, compute the checksum on
        the client, verify that the values match, and verify that the size is what you
        expected.

        A job ID does not expire for at least 24 hours after Amazon Glacier completes
        the job. That is, you can download the job output within the 24 hours period
        after Amazon Glacier completes the job.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and the underlying REST API, see [Downloading a Vault
        Inventory](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-
        inventory.html), [Downloading an
        Archive](http://docs.aws.amazon.com/amazonglacier/latest/dev/downloading-an-
        archive.html), and [Get Job Output
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-job-output-get.html)
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if job_id is not ShapeBase.NOT_SET:
                _params['job_id'] = job_id
            if range is not ShapeBase.NOT_SET:
                _params['range'] = range
            _request = shapes.GetJobOutputInput(**_params)
        response = self._boto_client.get_job_output(**_request.to_boto_dict())

        return shapes.GetJobOutputOutput.from_boto_dict(response)

    def get_vault_access_policy(
        self,
        _request: shapes.GetVaultAccessPolicyInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> shapes.GetVaultAccessPolicyOutput:
        """
        This operation retrieves the `access-policy` subresource set on the vault; for
        more information on setting this subresource, see [Set Vault Access Policy (PUT
        access-policy)](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-
        SetVaultAccessPolicy.html). If there is no access policy set on the vault, the
        operation returns a `404 Not found` error. For more information about vault
        access policies, see [Amazon Glacier Access Control with Vault Access
        Policies](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-access-
        policy.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.GetVaultAccessPolicyInput(**_params)
        response = self._boto_client.get_vault_access_policy(
            **_request.to_boto_dict()
        )

        return shapes.GetVaultAccessPolicyOutput.from_boto_dict(response)

    def get_vault_lock(
        self,
        _request: shapes.GetVaultLockInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> shapes.GetVaultLockOutput:
        """
        This operation retrieves the following attributes from the `lock-policy`
        subresource set on the specified vault:

          * The vault lock policy set on the vault.

          * The state of the vault lock, which is either `InProgess` or `Locked`.

          * When the lock ID expires. The lock ID is used to complete the vault locking process.

          * When the vault lock was initiated and put into the `InProgress` state.

        A vault lock is put into the `InProgress` state by calling InitiateVaultLock. A
        vault lock is put into the `Locked` state by calling CompleteVaultLock. You can
        abort the vault locking process by calling AbortVaultLock. For more information
        about the vault locking process, [Amazon Glacier Vault
        Lock](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-lock.html).

        If there is no vault lock policy set on the vault, the operation returns a `404
        Not found` error. For more information about vault lock policies, [Amazon
        Glacier Access Control with Vault Lock
        Policies](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-lock-
        policy.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.GetVaultLockInput(**_params)
        response = self._boto_client.get_vault_lock(**_request.to_boto_dict())

        return shapes.GetVaultLockOutput.from_boto_dict(response)

    def get_vault_notifications(
        self,
        _request: shapes.GetVaultNotificationsInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> shapes.GetVaultNotificationsOutput:
        """
        This operation retrieves the `notification-configuration` subresource of the
        specified vault.

        For information about setting a notification configuration on a vault, see
        SetVaultNotifications. If a notification configuration for a vault is not set,
        the operation returns a `404 Not Found` error. For more information about vault
        notifications, see [Configuring Vault Notifications in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/configuring-
        notifications.html).

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Configuring Vault
        Notifications in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/configuring-
        notifications.html) and [Get Vault Notification Configuration
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-vault-notifications-
        get.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.GetVaultNotificationsInput(**_params)
        response = self._boto_client.get_vault_notifications(
            **_request.to_boto_dict()
        )

        return shapes.GetVaultNotificationsOutput.from_boto_dict(response)

    def initiate_job(
        self,
        _request: shapes.InitiateJobInput = None,
        *,
        account_id: str,
        vault_name: str,
        job_parameters: shapes.JobParameters = ShapeBase.NOT_SET,
    ) -> shapes.InitiateJobOutput:
        """
        This operation initiates a job of the specified type, which can be a select, an
        archival retrieval, or a vault retrieval. For more information about using this
        operation, see the documentation for the underlying REST API [Initiate a
        Job](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-initiate-job-
        post.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if job_parameters is not ShapeBase.NOT_SET:
                _params['job_parameters'] = job_parameters
            _request = shapes.InitiateJobInput(**_params)
        response = self._boto_client.initiate_job(**_request.to_boto_dict())

        return shapes.InitiateJobOutput.from_boto_dict(response)

    def initiate_multipart_upload(
        self,
        _request: shapes.InitiateMultipartUploadInput = None,
        *,
        account_id: str,
        vault_name: str,
        archive_description: str = ShapeBase.NOT_SET,
        part_size: str = ShapeBase.NOT_SET,
    ) -> shapes.InitiateMultipartUploadOutput:
        """
        This operation initiates a multipart upload. Amazon Glacier creates a multipart
        upload resource and returns its ID in the response. The multipart upload ID is
        used in subsequent requests to upload parts of an archive (see
        UploadMultipartPart).

        When you initiate a multipart upload, you specify the part size in number of
        bytes. The part size must be a megabyte (1024 KB) multiplied by a power of 2-for
        example, 1048576 (1 MB), 2097152 (2 MB), 4194304 (4 MB), 8388608 (8 MB), and so
        on. The minimum allowable part size is 1 MB, and the maximum is 4 GB.

        Every part you upload to this resource (see UploadMultipartPart), except the
        last one, must have the same size. The last one can be the same size or smaller.
        For example, suppose you want to upload a 16.2 MB file. If you initiate the
        multipart upload with a part size of 4 MB, you will upload four parts of 4 MB
        each and one part of 0.2 MB.

        You don't need to know the size of the archive when you start a multipart upload
        because Amazon Glacier does not require you to specify the overall archive size.

        After you complete the multipart upload, Amazon Glacier removes the multipart
        upload resource referenced by the ID. Amazon Glacier also removes the multipart
        upload resource if you cancel the multipart upload or it may be removed if there
        is no activity for a period of 24 hours.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Uploading Large
        Archives in Parts (Multipart
        Upload)](http://docs.aws.amazon.com/amazonglacier/latest/dev/uploading-archive-
        mpu.html) and [Initiate Multipart
        Upload](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-multipart-
        initiate-upload.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if archive_description is not ShapeBase.NOT_SET:
                _params['archive_description'] = archive_description
            if part_size is not ShapeBase.NOT_SET:
                _params['part_size'] = part_size
            _request = shapes.InitiateMultipartUploadInput(**_params)
        response = self._boto_client.initiate_multipart_upload(
            **_request.to_boto_dict()
        )

        return shapes.InitiateMultipartUploadOutput.from_boto_dict(response)

    def initiate_vault_lock(
        self,
        _request: shapes.InitiateVaultLockInput = None,
        *,
        account_id: str,
        vault_name: str,
        policy: shapes.VaultLockPolicy = ShapeBase.NOT_SET,
    ) -> shapes.InitiateVaultLockOutput:
        """
        This operation initiates the vault locking process by doing the following:

          * Installing a vault lock policy on the specified vault.

          * Setting the lock state of vault lock to `InProgress`.

          * Returning a lock ID, which is used to complete the vault locking process.

        You can set one vault lock policy for each vault and this policy can be up to 20
        KB in size. For more information about vault lock policies, see [Amazon Glacier
        Access Control with Vault Lock
        Policies](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-lock-
        policy.html).

        You must complete the vault locking process within 24 hours after the vault lock
        enters the `InProgress` state. After the 24 hour window ends, the lock ID
        expires, the vault automatically exits the `InProgress` state, and the vault
        lock policy is removed from the vault. You call CompleteVaultLock to complete
        the vault locking process by setting the state of the vault lock to `Locked`.

        After a vault lock is in the `Locked` state, you cannot initiate a new vault
        lock for the vault.

        You can abort the vault locking process by calling AbortVaultLock. You can get
        the state of the vault lock by calling GetVaultLock. For more information about
        the vault locking process, [Amazon Glacier Vault
        Lock](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-lock.html).

        If this operation is called when the vault lock is in the `InProgress` state,
        the operation returns an `AccessDeniedException` error. When the vault lock is
        in the `InProgress` state you must call AbortVaultLock before you can initiate a
        new vault lock policy.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if policy is not ShapeBase.NOT_SET:
                _params['policy'] = policy
            _request = shapes.InitiateVaultLockInput(**_params)
        response = self._boto_client.initiate_vault_lock(
            **_request.to_boto_dict()
        )

        return shapes.InitiateVaultLockOutput.from_boto_dict(response)

    def list_jobs(
        self,
        _request: shapes.ListJobsInput = None,
        *,
        account_id: str,
        vault_name: str,
        limit: str = ShapeBase.NOT_SET,
        marker: str = ShapeBase.NOT_SET,
        statuscode: str = ShapeBase.NOT_SET,
        completed: str = ShapeBase.NOT_SET,
    ) -> shapes.ListJobsOutput:
        """
        This operation lists jobs for a vault, including jobs that are in-progress and
        jobs that have recently finished. The List Job operation returns a list of these
        jobs sorted by job initiation time.

        Amazon Glacier retains recently completed jobs for a period before deleting
        them; however, it eventually removes completed jobs. The output of completed
        jobs can be retrieved. Retaining completed jobs for a period of time after they
        have completed enables you to get a job output in the event you miss the job
        completion notification or your first attempt to download it fails. For example,
        suppose you start an archive retrieval job to download an archive. After the job
        completes, you start to download the archive but encounter a network error. In
        this scenario, you can retry and download the archive while the job exists.

        The List Jobs operation supports pagination. You should always check the
        response `Marker` field. If there are no more jobs to list, the `Marker` field
        is set to `null`. If there are more jobs to list, the `Marker` field is set to a
        non-null value, which you can use to continue the pagination of the list. To
        return a list of jobs that begins at a specific job, set the marker request
        parameter to the `Marker` value for that job that you obtained from a previous
        List Jobs request.

        You can set a maximum limit for the number of jobs returned in the response by
        specifying the `limit` parameter in the request. The default limit is 50. The
        number of jobs returned might be fewer than the limit, but the number of
        returned jobs never exceeds the limit.

        Additionally, you can filter the jobs list returned by specifying the optional
        `statuscode` parameter or `completed` parameter, or both. Using the `statuscode`
        parameter, you can specify to return only jobs that match either the
        `InProgress`, `Succeeded`, or `Failed` status. Using the `completed` parameter,
        you can specify to return only jobs that were completed (`true`) or jobs that
        were not completed (`false`).

        For more information about using this operation, see the documentation for the
        underlying REST API [List
        Jobs](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-jobs-get.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if limit is not ShapeBase.NOT_SET:
                _params['limit'] = limit
            if marker is not ShapeBase.NOT_SET:
                _params['marker'] = marker
            if statuscode is not ShapeBase.NOT_SET:
                _params['statuscode'] = statuscode
            if completed is not ShapeBase.NOT_SET:
                _params['completed'] = completed
            _request = shapes.ListJobsInput(**_params)
        response = self._boto_client.list_jobs(**_request.to_boto_dict())

        return shapes.ListJobsOutput.from_boto_dict(response)

    def list_multipart_uploads(
        self,
        _request: shapes.ListMultipartUploadsInput = None,
        *,
        account_id: str,
        vault_name: str,
        marker: str = ShapeBase.NOT_SET,
        limit: str = ShapeBase.NOT_SET,
    ) -> shapes.ListMultipartUploadsOutput:
        """
        This operation lists in-progress multipart uploads for the specified vault. An
        in-progress multipart upload is a multipart upload that has been initiated by an
        InitiateMultipartUpload request, but has not yet been completed or aborted. The
        list returned in the List Multipart Upload response has no guaranteed order.

        The List Multipart Uploads operation supports pagination. By default, this
        operation returns up to 50 multipart uploads in the response. You should always
        check the response for a `marker` at which to continue the list; if there are no
        more items the `marker` is `null`. To return a list of multipart uploads that
        begins at a specific upload, set the `marker` request parameter to the value you
        obtained from a previous List Multipart Upload request. You can also limit the
        number of uploads returned in the response by specifying the `limit` parameter
        in the request.

        Note the difference between this operation and listing parts (ListParts). The
        List Multipart Uploads operation lists all multipart uploads for a vault and
        does not require a multipart upload ID. The List Parts operation requires a
        multipart upload ID since parts are associated with a single upload.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and the underlying REST API, see [Working with
        Archives in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/working-with-
        archives.html) and [List Multipart Uploads
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-multipart-list-
        uploads.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if marker is not ShapeBase.NOT_SET:
                _params['marker'] = marker
            if limit is not ShapeBase.NOT_SET:
                _params['limit'] = limit
            _request = shapes.ListMultipartUploadsInput(**_params)
        response = self._boto_client.list_multipart_uploads(
            **_request.to_boto_dict()
        )

        return shapes.ListMultipartUploadsOutput.from_boto_dict(response)

    def list_parts(
        self,
        _request: shapes.ListPartsInput = None,
        *,
        account_id: str,
        vault_name: str,
        upload_id: str,
        marker: str = ShapeBase.NOT_SET,
        limit: str = ShapeBase.NOT_SET,
    ) -> shapes.ListPartsOutput:
        """
        This operation lists the parts of an archive that have been uploaded in a
        specific multipart upload. You can make this request at any time during an in-
        progress multipart upload before you complete the upload (see
        CompleteMultipartUpload. List Parts returns an error for completed uploads. The
        list returned in the List Parts response is sorted by part range.

        The List Parts operation supports pagination. By default, this operation returns
        up to 50 uploaded parts in the response. You should always check the response
        for a `marker` at which to continue the list; if there are no more items the
        `marker` is `null`. To return a list of parts that begins at a specific part,
        set the `marker` request parameter to the value you obtained from a previous
        List Parts request. You can also limit the number of parts returned in the
        response by specifying the `limit` parameter in the request.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and the underlying REST API, see [Working with
        Archives in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/working-with-
        archives.html) and [List
        Parts](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-multipart-list-
        parts.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if upload_id is not ShapeBase.NOT_SET:
                _params['upload_id'] = upload_id
            if marker is not ShapeBase.NOT_SET:
                _params['marker'] = marker
            if limit is not ShapeBase.NOT_SET:
                _params['limit'] = limit
            _request = shapes.ListPartsInput(**_params)
        response = self._boto_client.list_parts(**_request.to_boto_dict())

        return shapes.ListPartsOutput.from_boto_dict(response)

    def list_provisioned_capacity(
        self,
        _request: shapes.ListProvisionedCapacityInput = None,
        *,
        account_id: str,
    ) -> shapes.ListProvisionedCapacityOutput:
        """
        This operation lists the provisioned capacity units for the specified AWS
        account.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            _request = shapes.ListProvisionedCapacityInput(**_params)
        response = self._boto_client.list_provisioned_capacity(
            **_request.to_boto_dict()
        )

        return shapes.ListProvisionedCapacityOutput.from_boto_dict(response)

    def list_tags_for_vault(
        self,
        _request: shapes.ListTagsForVaultInput = None,
        *,
        account_id: str,
        vault_name: str,
    ) -> shapes.ListTagsForVaultOutput:
        """
        This operation lists all the tags attached to a vault. The operation returns an
        empty map if there are no tags. For more information about tags, see [Tagging
        Amazon Glacier
        Resources](http://docs.aws.amazon.com/amazonglacier/latest/dev/tagging.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            _request = shapes.ListTagsForVaultInput(**_params)
        response = self._boto_client.list_tags_for_vault(
            **_request.to_boto_dict()
        )

        return shapes.ListTagsForVaultOutput.from_boto_dict(response)

    def list_vaults(
        self,
        _request: shapes.ListVaultsInput = None,
        *,
        account_id: str,
        marker: str = ShapeBase.NOT_SET,
        limit: str = ShapeBase.NOT_SET,
    ) -> shapes.ListVaultsOutput:
        """
        This operation lists all vaults owned by the calling user's account. The list
        returned in the response is ASCII-sorted by vault name.

        By default, this operation returns up to 10 items. If there are more vaults to
        list, the response `marker` field contains the vault Amazon Resource Name (ARN)
        at which to continue the list with a new List Vaults request; otherwise, the
        `marker` field is `null`. To return a list of vaults that begins at a specific
        vault, set the `marker` request parameter to the vault ARN you obtained from a
        previous List Vaults request. You can also limit the number of vaults returned
        in the response by specifying the `limit` parameter in the request.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Retrieving Vault
        Metadata in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/retrieving-vault-
        info.html) and [List Vaults
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-vaults-get.html) in
        the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if marker is not ShapeBase.NOT_SET:
                _params['marker'] = marker
            if limit is not ShapeBase.NOT_SET:
                _params['limit'] = limit
            _request = shapes.ListVaultsInput(**_params)
        response = self._boto_client.list_vaults(**_request.to_boto_dict())

        return shapes.ListVaultsOutput.from_boto_dict(response)

    def purchase_provisioned_capacity(
        self,
        _request: shapes.PurchaseProvisionedCapacityInput = None,
        *,
        account_id: str,
    ) -> shapes.PurchaseProvisionedCapacityOutput:
        """
        This operation purchases a provisioned capacity unit for an AWS account.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            _request = shapes.PurchaseProvisionedCapacityInput(**_params)
        response = self._boto_client.purchase_provisioned_capacity(
            **_request.to_boto_dict()
        )

        return shapes.PurchaseProvisionedCapacityOutput.from_boto_dict(response)

    def remove_tags_from_vault(
        self,
        _request: shapes.RemoveTagsFromVaultInput = None,
        *,
        account_id: str,
        vault_name: str,
        tag_keys: typing.List[str] = ShapeBase.NOT_SET,
    ) -> None:
        """
        This operation removes one or more tags from the set of tags attached to a
        vault. For more information about tags, see [Tagging Amazon Glacier
        Resources](http://docs.aws.amazon.com/amazonglacier/latest/dev/tagging.html).
        This operation is idempotent. The operation will be successful, even if there
        are no tags attached to the vault.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if tag_keys is not ShapeBase.NOT_SET:
                _params['tag_keys'] = tag_keys
            _request = shapes.RemoveTagsFromVaultInput(**_params)
        response = self._boto_client.remove_tags_from_vault(
            **_request.to_boto_dict()
        )

    def set_data_retrieval_policy(
        self,
        _request: shapes.SetDataRetrievalPolicyInput = None,
        *,
        account_id: str,
        policy: shapes.DataRetrievalPolicy = ShapeBase.NOT_SET,
    ) -> None:
        """
        This operation sets and then enacts a data retrieval policy in the region
        specified in the PUT request. You can set one policy per region for an AWS
        account. The policy is enacted within a few minutes of a successful PUT
        operation.

        The set policy operation does not affect retrieval jobs that were in progress
        before the policy was enacted. For more information about data retrieval
        policies, see [Amazon Glacier Data Retrieval
        Policies](http://docs.aws.amazon.com/amazonglacier/latest/dev/data-retrieval-
        policy.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if policy is not ShapeBase.NOT_SET:
                _params['policy'] = policy
            _request = shapes.SetDataRetrievalPolicyInput(**_params)
        response = self._boto_client.set_data_retrieval_policy(
            **_request.to_boto_dict()
        )

    def set_vault_access_policy(
        self,
        _request: shapes.SetVaultAccessPolicyInput = None,
        *,
        account_id: str,
        vault_name: str,
        policy: shapes.VaultAccessPolicy = ShapeBase.NOT_SET,
    ) -> None:
        """
        This operation configures an access policy for a vault and will overwrite an
        existing policy. To configure a vault access policy, send a PUT request to the
        `access-policy` subresource of the vault. An access policy is specific to a
        vault and is also called a vault subresource. You can set one access policy per
        vault and the policy can be up to 20 KB in size. For more information about
        vault access policies, see [Amazon Glacier Access Control with Vault Access
        Policies](http://docs.aws.amazon.com/amazonglacier/latest/dev/vault-access-
        policy.html).
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if policy is not ShapeBase.NOT_SET:
                _params['policy'] = policy
            _request = shapes.SetVaultAccessPolicyInput(**_params)
        response = self._boto_client.set_vault_access_policy(
            **_request.to_boto_dict()
        )

    def set_vault_notifications(
        self,
        _request: shapes.SetVaultNotificationsInput = None,
        *,
        account_id: str,
        vault_name: str,
        vault_notification_config: shapes.VaultNotificationConfig = ShapeBase.
        NOT_SET,
    ) -> None:
        """
        This operation configures notifications that will be sent when specific events
        happen to a vault. By default, you don't get any notifications.

        To configure vault notifications, send a PUT request to the `notification-
        configuration` subresource of the vault. The request should include a JSON
        document that provides an Amazon SNS topic and specific events for which you
        want Amazon Glacier to send notifications to the topic.

        Amazon SNS topics must grant permission to the vault to be allowed to publish
        notifications to the topic. You can configure a vault to publish a notification
        for the following vault events:

          * **ArchiveRetrievalCompleted** This event occurs when a job that was initiated for an archive retrieval is completed (InitiateJob). The status of the completed job can be "Succeeded" or "Failed". The notification sent to the SNS topic is the same output as returned from DescribeJob. 

          * **InventoryRetrievalCompleted** This event occurs when a job that was initiated for an inventory retrieval is completed (InitiateJob). The status of the completed job can be "Succeeded" or "Failed". The notification sent to the SNS topic is the same output as returned from DescribeJob. 

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Configuring Vault
        Notifications in Amazon
        Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/configuring-
        notifications.html) and [Set Vault Notification Configuration
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-vault-notifications-
        put.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if vault_notification_config is not ShapeBase.NOT_SET:
                _params['vault_notification_config'] = vault_notification_config
            _request = shapes.SetVaultNotificationsInput(**_params)
        response = self._boto_client.set_vault_notifications(
            **_request.to_boto_dict()
        )

    def upload_archive(
        self,
        _request: shapes.UploadArchiveInput = None,
        *,
        vault_name: str,
        account_id: str,
        archive_description: str = ShapeBase.NOT_SET,
        checksum: str = ShapeBase.NOT_SET,
        body: typing.Any = ShapeBase.NOT_SET,
    ) -> shapes.ArchiveCreationOutput:
        """
        This operation adds an archive to a vault. This is a synchronous operation, and
        for a successful upload, your data is durably persisted. Amazon Glacier returns
        the archive ID in the `x-amz-archive-id` header of the response.

        You must use the archive ID to access your data in Amazon Glacier. After you
        upload an archive, you should save the archive ID returned so that you can
        retrieve or delete the archive later. Besides saving the archive ID, you can
        also index it and give it a friendly name to allow for better searching. You can
        also use the optional archive description field to specify how the archive is
        referred to in an external index of archives, such as you might create in Amazon
        DynamoDB. You can also get the vault inventory to obtain a list of archive IDs
        in a vault. For more information, see InitiateJob.

        You must provide a SHA256 tree hash of the data you are uploading. For
        information about computing a SHA256 tree hash, see [Computing
        Checksums](http://docs.aws.amazon.com/amazonglacier/latest/dev/checksum-
        calculations.html).

        You can optionally specify an archive description of up to 1,024 printable ASCII
        characters. You can get the archive description when you either retrieve the
        archive or get the vault inventory. For more information, see InitiateJob.
        Amazon Glacier does not interpret the description in any way. An archive
        description does not need to be unique. You cannot use the description to
        retrieve or sort the archive list.

        Archives are immutable. After you upload an archive, you cannot edit the archive
        or its description.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Uploading an Archive in
        Amazon Glacier](http://docs.aws.amazon.com/amazonglacier/latest/dev/uploading-
        an-archive.html) and [Upload
        Archive](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-archive-
        post.html) in the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if archive_description is not ShapeBase.NOT_SET:
                _params['archive_description'] = archive_description
            if checksum is not ShapeBase.NOT_SET:
                _params['checksum'] = checksum
            if body is not ShapeBase.NOT_SET:
                _params['body'] = body
            _request = shapes.UploadArchiveInput(**_params)
        response = self._boto_client.upload_archive(**_request.to_boto_dict())

        return shapes.ArchiveCreationOutput.from_boto_dict(response)

    def upload_multipart_part(
        self,
        _request: shapes.UploadMultipartPartInput = None,
        *,
        account_id: str,
        vault_name: str,
        upload_id: str,
        checksum: str = ShapeBase.NOT_SET,
        range: str = ShapeBase.NOT_SET,
        body: typing.Any = ShapeBase.NOT_SET,
    ) -> shapes.UploadMultipartPartOutput:
        """
        This operation uploads a part of an archive. You can upload archive parts in any
        order. You can also upload them in parallel. You can upload up to 10,000 parts
        for a multipart upload.

        Amazon Glacier rejects your upload part request if any of the following
        conditions is true:

          * **SHA256 tree hash does not match** To ensure that part data is not corrupted in transmission, you compute a SHA256 tree hash of the part and include it in your request. Upon receiving the part data, Amazon Glacier also computes a SHA256 tree hash. If these hash values don't match, the operation fails. For information about computing a SHA256 tree hash, see [Computing Checksums](http://docs.aws.amazon.com/amazonglacier/latest/dev/checksum-calculations.html).

          * **Part size does not match** The size of each part except the last must match the size specified in the corresponding InitiateMultipartUpload request. The size of the last part must be the same size as, or smaller than, the specified size.

        If you upload a part whose size is smaller than the part size you specified in
        your initiate multipart upload request and that part is not the last part, then
        the upload part request will succeed. However, the subsequent Complete Multipart
        Upload request will fail.

          * **Range does not align** The byte range value in the request does not align with the part size specified in the corresponding initiate request. For example, if you specify a part size of 4194304 bytes (4 MB), then 0 to 4194303 bytes (4 MB - 1) and 4194304 (4 MB) to 8388607 (8 MB - 1) are valid part ranges. However, if you set a range value of 2 MB to 6 MB, the range does not align with the part size and the upload will fail. 

        This operation is idempotent. If you upload the same part multiple times, the
        data included in the most recent request overwrites the previously uploaded
        data.

        An AWS account has full permission to perform all operations (actions). However,
        AWS Identity and Access Management (IAM) users don't have any permissions by
        default. You must grant them explicit permission to perform specific actions.
        For more information, see [Access Control Using AWS Identity and Access
        Management (IAM)](http://docs.aws.amazon.com/amazonglacier/latest/dev/using-iam-
        with-amazon-glacier.html).

        For conceptual information and underlying REST API, see [Uploading Large
        Archives in Parts (Multipart
        Upload)](http://docs.aws.amazon.com/amazonglacier/latest/dev/uploading-archive-
        mpu.html) and [Upload Part
        ](http://docs.aws.amazon.com/amazonglacier/latest/dev/api-upload-part.html) in
        the _Amazon Glacier Developer Guide_.
        """
        if _request is None:
            _params = {}
            if account_id is not ShapeBase.NOT_SET:
                _params['account_id'] = account_id
            if vault_name is not ShapeBase.NOT_SET:
                _params['vault_name'] = vault_name
            if upload_id is not ShapeBase.NOT_SET:
                _params['upload_id'] = upload_id
            if checksum is not ShapeBase.NOT_SET:
                _params['checksum'] = checksum
            if range is not ShapeBase.NOT_SET:
                _params['range'] = range
            if body is not ShapeBase.NOT_SET:
                _params['body'] = body
            _request = shapes.UploadMultipartPartInput(**_params)
        response = self._boto_client.upload_multipart_part(
            **_request.to_boto_dict()
        )

        return shapes.UploadMultipartPartOutput.from_boto_dict(response)
