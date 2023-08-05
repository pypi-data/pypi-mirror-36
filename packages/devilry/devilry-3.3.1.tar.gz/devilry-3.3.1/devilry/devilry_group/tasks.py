# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from pprint import pprint

from ievv_opensource.ievv_batchframework import batchregistry


class AbstractBaseBatchAction(batchregistry.Action):
    """
    """
    #: Backend id to get from registry in function `get_backend()`.
    #: Must be set in subclass.
    backend_id = ''

    def get_backend(self, zipfile_path, archive_name):
        """
        Get and instance of the backend to use.

        Args:
            zipfile_path: Path to the archive.
            archive_name: Name of the archive.

        Returns:
            PythonZipFileBackend: Backend for `self.backend_id`
        """
        from devilry.devilry_compressionutil import backend_registry
        zipfile_backend_class = backend_registry.Registry.get_instance().get(self.backend_id)
        return zipfile_backend_class(
            archive_path=zipfile_path,
            archive_name=archive_name,
            readmode=False
        )

    def add_file(self, zipfile_backend, sub_path, comment_file, is_duplicate=False):
        """
        Add file to ZIP archive.

        Args:
            zipfile_backend: A subclass of ``PythonZipFileBackend``.
            sub_path: The path to write to inside the archive.
            comment_file: The `CommentFile` file to write.
            is_duplicate: Is the file a duplicate? Defaults to ``False``.
        """
        file_name = comment_file.filename
        if is_duplicate:
            file_name = comment_file.get_filename_as_unique_string()

        zipfile_backend.add_file(
            os.path.join(sub_path, file_name),
            comment_file.file.file)

    def execute(self):
        raise NotImplementedError()


class FeedbackSetBatchMixin(object):
    """
    Mixin for adding FeedbackSet files to zipfile.

    Must be included in class together with :class:`~.AbstractBaseBatchAction`.
    """
    def __build_zip_archive_from_comment_file_tree(self, zipfile_backend, sub_path,
                                                   comment_file_tree, deadline_datetime):
        for filename, value in comment_file_tree.iteritems():
            # Add files before deadline
            if value['before_deadline']['last']:
                comment_file = value['before_deadline']['last']
                self.add_file(zipfile_backend=zipfile_backend,
                              sub_path=sub_path,
                              comment_file=comment_file)
                for old_duplicate in value['before_deadline']['old_duplicates']:
                    self.add_file(zipfile_backend=zipfile_backend,
                                  sub_path=os.path.join(sub_path, 'old_duplicates'),
                                  comment_file=old_duplicate,
                                  is_duplicate=True)

            # Add files after deadline
            if value['after_deadline']['last']:
                comment_file = value['after_deadline']['last']
                after_deadline_sub_path = os.path.join(sub_path, 'after_deadline_not_part_of_delivery')
                self.add_file(zipfile_backend=zipfile_backend,
                              sub_path=after_deadline_sub_path,
                              comment_file=comment_file)
                for old_duplicate in value['after_deadline']['old_duplicates']:
                    self.add_file(zipfile_backend=zipfile_backend,
                                  sub_path=os.path.join(after_deadline_sub_path, 'old_duplicates'),
                                  comment_file=old_duplicate,
                                  is_duplicate=True)

    def zipfile_add_feedbackset(self, zipfile_backend, feedback_set, sub_path=''):
        from devilry.devilry_group import models as group_models

        comment_file_tree = {}
        for group_comment in feedback_set.groupcomment_set.all().order_by('-created_datetime'):
            # Don't add files from comments that are not visible to everyone.
            if group_comment.visibility == group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE and \
                    group_comment.user_role == group_models.GroupComment.USER_ROLE_STUDENT:
                for comment_file in group_comment.commentfile_set.all().order_by('-created_datetime'):
                    filename = comment_file.filename
                    if comment_file.filename not in comment_file_tree:
                        comment_file_tree[filename] = {
                            'before_deadline': {
                                'last': None,
                                'old_duplicates': []
                            },
                            'after_deadline': {
                                'last': None,
                                'old_duplicates': []
                            }
                        }

                    if group_comment.published_datetime <= feedback_set.deadline_datetime:
                        # Before the deadline expired
                        # Set initial last delivery before deadline, and duplicates.
                        if comment_file_tree[filename]['before_deadline']['last'] is None:
                            comment_file_tree[filename]['before_deadline']['last'] = comment_file
                        else:
                            comment_file_tree[filename]['before_deadline']['old_duplicates'].append(comment_file)

                    else:
                        # After the deadline expired.
                        # Set initial last delivery after deadline, and duplicates.
                        if comment_file_tree[filename]['after_deadline']['last'] is None:
                            comment_file_tree[filename]['after_deadline']['last'] = comment_file
                        else:
                            comment_file_tree[filename]['after_deadline']['old_duplicates'].append(comment_file)

        # Start building the ZIP archive.
        self.__build_zip_archive_from_comment_file_tree(
            zipfile_backend=zipfile_backend,
            sub_path=sub_path,
            comment_file_tree=comment_file_tree,
            deadline_datetime=feedback_set.deadline_datetime
        )


class FeedbackSetCompressAction(AbstractBaseBatchAction, FeedbackSetBatchMixin):
    """
    Compress all files that belong to a :obj:`~devilry_group.models.FeedbackSet`.
    """
    backend_id = 'devilry_group_local'

    def execute(self):
        feedback_set = self.kwargs.get('context_object')
        started_by_user = self.kwargs.get('started_by')

        from devilry.devilry_group import models as group_models
        feedback_sets_with_public_student_comments = group_models.FeedbackSet.objects\
            .filter_public_comment_files_from_students().filter(id=feedback_set.id)
        if not feedback_sets_with_public_student_comments.exists():
            # Do nothing
            return

        # Create the name for the actual archive.
        from django.utils import timezone
        archive_name = 'feedbackset-{}-{}-delivery.zip'.format(
            feedback_set.id,
            timezone.now().strftime('%Y-%m-%d_%H-%M-%S.%f'))

        # create the path for the archive
        zipfile_path = os.path.join(
            str(feedback_set.group.parentnode.parentnode_id),
            str(feedback_set.group.parentnode.id),
            str(feedback_set.group.id),
            archive_name)

        # Get backend
        zipfile_backend = self.get_backend(zipfile_path=zipfile_path, archive_name=archive_name)

        # Add FeedbackSet files to archive.
        self.zipfile_add_feedbackset(zipfile_backend=zipfile_backend, feedback_set=feedback_set)

        zipfile_backend.close()

        # create archive meta entry
        from devilry.devilry_compressionutil.models import CompressedArchiveMeta
        CompressedArchiveMeta.objects.create_meta(
            instance=feedback_set,
            zipfile_backend=zipfile_backend,
            user=started_by_user
        )
