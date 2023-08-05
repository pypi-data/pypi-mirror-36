# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File for operating on a Oracle Subclient

OracleSubclient is the only class defined in this file.

OracleSubclient: Derived class from DatabaseSubclient Base class, representing an Oracle subclient,
                        and to perform operations on that subclient

OracleSubclient:
    __init__()                          -- constructor for the class

    data_sp()                           -- Getters and setters for data storage policy

    _get_oracle_restore_json            -- Method to get restore JSON for an oracle instance

    _oracle_cumulative_backup_json      -- Get cumulative backup JSON for oracle instance

    is_snapenabled()                    -- Check if intellisnap has been enabled in the subclient

    backup                              -- Method to backup database

    restore                             -- Method to restore databases

"""
from __future__ import unicode_literals
from .dbsubclient import DatabaseSubclient
from ..exception import SDKException
from ..constants import InstanceBackupType


class OracleSubclient(DatabaseSubclient):
    """
    OracleSubclient is a class to work on Oracle subclients

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Constructor for the class

        Args:
            backupset_object  (object)  -- instance of the Backupset class
            subclient_name    (str)     -- name of the subclient
            subclient_id      (str)     -- id of the subclient
        """
        super(OracleSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self._oracle_properties = {}

    def _oracle_cumulative_backup_json(self):
        """
        Method to add oracle options to oracle backup

        Returns:
            dict    -- dict containing request JSON

        """
        oracle_options = {
            "oracleOptions": {}
        }
        request_json = self._backup_json(InstanceBackupType.CUMULATIVE, False, "BEFORE SYNTH")

        # Add option to run RMAN cumulatives
        oracle_options["oracleOptions"]["cumulative"] = True

        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
            oracle_options
        )
        return request_json

    @property
    def data_sp(self):
        """
        Getter for data storage policy

        Returns:
            string - string representing data storage policy
        """
        return self._commonProperties['storageDevice']['dataBackupStoragePolicy']['storagePolicyName']

    @property
    def is_snapenabled(self):
        """
        Getter to check whether the subclient has snap enabled

        Returns:
            Bool - True if snap is enabled on the subclient. Else False
        """
        return self._commonProperties['snapCopyInfo']['isSnapBackupEnabled']

    @property
    def find(self, *args, **kwargs):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__, 'find'))

    def backup(self, backup_level=InstanceBackupType.FULL.value, cumulative=False):
        """

        Args:
            cumulative (Bool) -- True if cumulative backup is required
                default: False
            backup_level (str)  -- Level of backup. Can be full or incremental
                default: full

        Returns:
            object -- instance of Job class

        Raises:
            SDKException:
                if backup level is incorrect

                if response is empty

                if response does not succeed

        """
        if backup_level not in ['full', 'incremental']:
            raise SDKException(r'Subclient', r'103')

        if not cumulative:
            return super(OracleSubclient, self).backup(backup_level)

        request_json = self._oracle_cumulative_backup_json()
        backup_service = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_service, request_json
        )
        return self._process_backup_response(flag, response)

    def restore(self, common_options=None,
                destination_client=None,
                oracle_options=None):
        """
        Method to restore the entire database using latest backup

        Args:
            destination_client (str) -- destination client name
            common_options (str) -- common options to be passed on for restore
                default -- None
            oracle_options (dict): dictionary containing other oracle options
                default -- By default it restores the controlfile and datafiles
                                from latest backup
                Example: {
                            "resetLogs": 1,
                            "switchDatabaseMode": True,
                            "noCatalog": True,
                            "restoreControlFile": True,
                            "recover": True,
                            "recoverFrom": 3,
                            "restoreData": True,
                            "restoreFrom": 3
                        }
        Returns:
            object -- Job containing restore details
        """
        return self._backupset_object._instance_object.restore(destination_client,
                                                               common_options,
                                                               oracle_options)
