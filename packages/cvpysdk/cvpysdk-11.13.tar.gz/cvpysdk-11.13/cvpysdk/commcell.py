# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations on Commcell via REST API.

Commcell is the main class for the CVPySDK python package.

Commcell:   Initializes a connection to the commcell and is a wrapper for the entire commcell ops.

Commcell:
    __init__()                  --  initialize instance of the Commcell class

    __repr__()                  --  return the name of the commcell, user is connected to,
    along with the user name of the connected user

    __enter__()                 --  returns the current instance, using the "with" context manager

    __exit__()                  --  logs out the user associated with the current instance

    _update_response_()         --  returns only the relevant response for the response received
    from the server

    _remove_attribs_()          --  removes all the attributs associated with the commcell
    object upon call to the logout method

    _get_commserv_details()     --  gets the details of the commserv, the Commcell class instance
    is initialized for

    _qoperation_execute()       --  runs the qoperation execute rest api on specified input xml

    _qoperation_execscript()    --  runs the qoperation execute script rest api with
    specified arguements

    _set_gxglobalparam_value    --  updates GXGlobalParam(commcell level configuration parameters)

    logout()                    --  logs out the user associated with the current instance

    request()                   --  runs an input HTTP request on the API specified,
    and returns its response

    send_mail()                 --  sends an email to the specified user

    refresh()                   --  refresh the properties associated with the Commcell
    class instance
    run_data_aging()            --  triggers data aging job from the commcell level

    get_saml_token()            --  returns the SAML token for the currently logged-in user

    add_additional_setting()    --  adds registry key to the commserve property

    delete_additional_setting() --  deletes registry key from the commserve property

Commcell instance Attributes
============================

    **commserv_guid**           --  returns the `CommServ` GUID, class instance is initalized for

    **commserv_hostname**       --  returns the hostname of the `CommServ`, class instance is
    initalized for

    **commserv_name**           --  returns the `CommServ` name, class instance is initalized for

    **commserv_timezone**       --  returns the time zone of the `CommServ`,
    class instance is initalized for

    **commserv_timezone_name**  --  returns the name of the `CommServ` time zone,
    class instance is initalized for

    **commserv_version**        --  returns the ContentStore version installed on the `CommServ`,
    class instance is initalized for

    **commcell_id**             --  returns the `CommCell` ID

    **webconsole_hostname**     --  returns the host name of the `webconsole`,
    class instance is connected to

    **auth_token**              --  returns the `Authtoken` for the current session to the commcell

    **commcell_username**       --  returns the associated `user` name for the current session
    to the commcell

    **device_id**               --  returns the id associated with the calling machine

    **clients**                 --  returns the instance of the `Clients` class,
    to interact with the clients added on the Commcell

    **media_agents**            --  returns the instance of the `MediaAgents` class,
    to interact with the media agents associated with the Commcell class instance

    **workflows**               --  returns the instance of the `WorkFlow` class,
    to interact with the workflows deployed on the Commcell

    **alerts**                  --  returns the instance of the `Alerts` class,
    to interact with the alerts available on the Commcell

    **disk_libraries**          --  returns the instance of the `DiskLibraries` class,
    to interact with the disk libraries added on the Commcell

    **storage_policies**        --  returns the instance of the `StoragePolicies` class,
    to interact with the storage policies available on the Commcell

    **schedule_policies**       --  returns the instance of the `SchedulePolicies` class,
    to interact with the schedule policies added to the Commcell

    **user_groups**             --  returns the instance of the `UserGroups` class,
    to interact with the user groups added to the Commcell

    **domains**                 --  returns the instance of the `Domains` class,
    to interact with the domains added to the Commcell

    **client_groups**           --  returns the instance of the `ClientGroups` class,
    to interact with the client groups added to the Commcell

    **global_filters**          --  returns the instance of the `GlobalFilters` class,
    to interact with the global filters available on the Commcell

    **datacube**                --  returns the instance of the `Datacube` class,
    to interact with the datacube engine deployed on the Commcell

    **plans**                   --  returns the instance of the `Plans` class,
    to interact with the plans associated with the Commcell

    **job_controller**          --  returns the instance of the `JobController` class,
    to interact with all the jobs finished / running on the Commcell

    **users**                   --  returns the instance of the `Users` class,
    to interact with the users added to the Commcell

    **roles**                   --  returns the instance of the `Roles` class,
    to interact with the roles added to the Commcell

    **download_center**         --  returns the instance of the `DownloadCenter` class,
    to interact with the download center repositories deployed on the Commcell WebConsole

    **organizations**           --  returns the instance of the `Organizations` class,
    to interact with the organizations/companies added on the Commcell

    **storage_pools**           --  returns the instance of the `StoragePools` class,
    to interact with the storage pools added to the Commcell Admin Console

    **monitoring_policies**     --  returns the instance of the `MonitoringPolicies` class,
    to interact with the MonitoringPolicies added to the Commcell

    **operation_window**        -- returns the instance of the 'OperationWindow' class,
    to interact with the opeartion windows of commcell

    **array_management**        --  returns the instance of the `ArrayManagement` class,
    to perform SNAP related operations on the Commcell

    **activity_control**        --  returns the instance of the `ActivityControl` class,
    to interact with the Activity Control on the Commcell

    **event_viewer**            --  returns the instance of the `Events` class,
    to interact with the Events associated on the Commcell

    **disasterrecovery**    -- returns the instance of the 'DisasterRecovery' class,
    to run disaster recovery backup , restore operations.

    **commserv_client**         --  returns the client object associated with the
    commserver

    **Commcell_Migration**      --  returns the instance of the 'CommCellMigration' class,
    to interact with the Commcell Export & Import on the Commcell
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import getpass
import socket

from base64 import b64encode

from requests.exceptions import SSLError
from requests.exceptions import Timeout

# ConnectionError is a built-in exception, do not override it
from requests.exceptions import ConnectionError as RequestsConnectionError


from .services import get_services
from .cvpysdk import CVPySDK
from .client import Clients
from .alert import Alerts
from .storage import MediaAgents
from .storage import DiskLibraries
from .security.usergroup import UserGroups
from .domains import Domains
from .workflow import WorkFlows
from .exception import SDKException
from .clientgroup import ClientGroups
from .globalfilter import GlobalFilters
from .datacube.datacube import Datacube
from .plan import Plans
from .job import JobController
from .security.user import Users
from .security.role import Roles
from .download_center import DownloadCenter
from .organization import Organizations
from .storage_pool import StoragePools
from .monitoring import MonitoringPolicies
from .policy import Policies
from .schedules import SchedulePattern
from .schedules import Schedule
from .activitycontrol import ActivityControl
from .eventviewer import Events
from .array_management import ArrayManagement
from .disasterrecovery import DisasterRecovery
from .operation_window import OperationWindow
from .commcell_migration import CommCellMigration


USER_LOGGED_OUT_MESSAGE = 'User Logged Out. Please initialize the Commcell object again.'
"""str:     Message to be returned to the user, when trying the get the value of an attribute
of the Commcell class, after the user was logged out.

"""


class Commcell(object):
    """Class for establishing a session to the Commcell via Commvault REST API."""

    def __init__(
            self,
            webconsole_hostname,
            commcell_username=None,
            commcell_password=None,
            authtoken=None):
        """Initialize the Commcell object with the values required for doing the API operations.

            Commcell Username and Password can be None, if QSDK / SAML token is being given
            as the input by the user.

            If both the Commcell Password and the Authtoken are None,
            then the user will be prompted to enter the password via command line.


            Args:
                webconsole_hostname     (str)   --  webconsole host Name / IP address

                    e.g.:

                        -   webclient.company.com

                        -   xxx.xxx.xxx.xxx


                commcell_username       (str)   --  username for log in to the commcell console

                    default: None


                commcell_password       (str)   --  plain-text password for log in to the console

                    default: None


                authtoken               (str)   --  QSDK / SAML token for log in to the console

                    default: None


            Returns:
                object  -   instance of this class

            Raises:
                SDKException:
                    if the web service is down or not reachable

                    if no token is received upon log in

        """
        web_service = [
            r'https://{0}/webconsole/api/'.format(webconsole_hostname),
            r'http://{0}/webconsole/api/'.format(webconsole_hostname)
        ]

        self._user = commcell_username

        self._password = None

        self._headers = {
            'Host': webconsole_hostname,
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authtoken': None
        }

        self._device_id = socket.getfqdn()

        self._cvpysdk_object = CVPySDK(self)

        # Checks if the service is running or not
        for service in web_service:
            self._web_service = service
            try:
                if self._cvpysdk_object._is_valid_service():
                    break
            except (RequestsConnectionError, SSLError, Timeout):
                continue
        else:
            raise SDKException('Commcell', '101')

        # Initialize all the services with this commcell service
        self._services = get_services(self._web_service)

        validity_err = None
        self._is_saml_login = False

        if isinstance(commcell_password, dict):
            authtoken = commcell_password['Authtoken']

        if authtoken:
            if authtoken.startswith('QSDK ') or authtoken.startswith('SAML '):
                self._headers['Authtoken'] = authtoken
            else:
                self._headers['Authtoken'] = '{0}{1}'.format('QSDK ', authtoken)

            try:
                self._user = self._cvpysdk_object.who_am_i()
                self._is_saml_login = True if authtoken.startswith('SAML ') else False
            except SDKException as error:
                self._headers['Authtoken'] = None
                validity_err = error

        if not self._headers['Authtoken'] and commcell_username is not None:
            if commcell_password is None:
                commcell_password = getpass.getpass('Please enter the Commcell Password: ')

            self._password = b64encode(commcell_password.encode()).decode()
            # Login to the commcell with the credentials provided
            # and store the token in the headers
            self._headers['Authtoken'] = self._cvpysdk_object._login()

        if not self._headers['Authtoken']:
            if isinstance(validity_err, Exception):
                raise validity_err

            raise SDKException('Commcell', '102')

        self._commserv_name = None
        self._commserv_hostname = None
        self._commserv_timezone = None
        self._commserv_timezone_name = None
        self._commserv_guid = None
        self._commserv_version = None

        self._id = None
        self._clients = None
        self._media_agents = None
        self._workflows = None
        self._disaster_recovery = None
        self._alerts = None
        self._disk_libraries = None
        self._storage_policies = None
        self._schedule_policies = None
        self._policies = None
        self._user_groups = None
        self._domains = None
        self._client_groups = None
        self._global_filters = None
        self._datacube = None
        self._plans = None
        self._job_controller = None
        self._users = None
        self._roles = None
        self._download_center = None
        self._organizations = None
        self._storage_pools = None
        self._activity_control = None
        self._events = None
        self._monitoring_policies = None
        self._array_management = None
        self._operation_window = None
        self._commserv_client = None
        self._commcell_migration = None

        self.refresh()

        del self._password

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string about the details of the Commcell class instance

        """
        representation_string = 'Commcell class instance of Commcell: "{0}", for User: "{1}"'
        return representation_string.format(self.commserv_name, self._user)

    def __enter__(self):
        """Returns the current instance.

            Returns:
                object  -   the initialized instance referred by self

        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Logs out the user associated with the current instance."""
        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def _update_response_(self, input_string):
        """Returns only the relevant response from the response received from the server.

            Args:
                input_string    (str)   --  input string to retrieve the relevant response from

            Returns:
                str     -   final response to be used

        """
        if '<title>' in input_string and '</title>' in input_string:
            response_string = input_string.split("<title>")[1]
            response_string = response_string.split("</title>")[0]
            return response_string

        return input_string

    def _remove_attribs_(self):
        """Removes all the attributes associated with the instance of this class."""
        del self._clients
        del self._media_agents
        del self._workflows
        del self._alerts
        del self._disk_libraries
        del self._storage_policies
        del self._schedule_policies
        del self._user_groups
        del self._policies
        del self._domains
        del self._roles
        del self._client_groups
        del self._global_filters
        del self._datacube
        del self._plans
        del self._job_controller
        del self._users
        del self._download_center
        del self._organizations
        del self._storage_pools
        del self._activity_control
        del self._events
        del self._monitoring_policies
        del self._array_management
        del self._operation_window
        del self._commserv_client

        del self._web_service
        del self._cvpysdk_object
        del self._device_id
        del self._services
        del self._disaster_recovery
        del self._commcell_migration
        del self

    def _get_commserv_details(self):
        """Gets the details of the CommServ, the Commcell class instance is initialized for,
            and updates the class instance attributes.

            Returns:
                None

            Raises:
                SDKException:
                    if failed to get commserv details

                    if response received is empty

                    if response is not success

        """
        import re

        flag, response = self._cvpysdk_object.make_request('GET', self._services['COMMSERV'])

        if flag:
            if response.json():
                try:
                    self._commserv_guid = response.json()['commcell']['csGUID']
                    self._commserv_hostname = response.json()['hostName']
                    self._commserv_name = response.json()['commcell']['commCellName']
                    self._commserv_timezone_name = response.json()['csTimeZone']['TimeZoneName']
                    self._commserv_version = response.json()['currentSPVersion']
                    self._id = response.json()['commcell']['commCellId']

                    self._commserv_timezone = re.search(
                        r'\(.*', response.json()['timeZone']
                    ).group()
                except KeyError as error:
                    raise SDKException('Commcell', '103', 'Key does not exist: {0}'.format(error))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _qoperation_execute(self, request_xml):
        """Makes a qoperation execute rest api call

            Args:
                request_xml     (str)   --  request xml that is to be passed

            Returns:
                dict    -   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @staticmethod
    def _convert_days_to_epoch(days):
        """
        convert the days to epoch time stamp
        Args:
            days: Number of days to convert

        Returns:
            from_time : days - now  . start time in unix format
            to_time   : now . end time in unix format
        """
        import datetime
        import time
        now = datetime.datetime.now()
        then = now - datetime.timedelta(days=days)
        start_dt = time.mktime(then.timetuple())
        end_dt = time.mktime(now.timetuple())
        return start_dt, end_dt

    @property
    def commcell_id(self):
        """Returns the ID of the CommCell."""
        return self._id

    def _qoperation_execscript(self, arguments):
        """Makes a qoperation execute rest api call

            Args:
                arguments     (str)   --  arguements that is to be passed

            Returns:
                dict    -   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QSCRIPT'] % arguments)

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _set_gxglobalparam_value(self, request_json):
        """ Updates GXGlobalParam table (Commcell level configuration parameters)

            Args:
                request_json (str)   --  request json that is to be passed

            Returns:
                dict                --   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GLOBAL_PARAM'], request_json
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def commserv_guid(self):
        """Returns the GUID of the CommServ."""
        return self._commserv_guid

    @property
    def commserv_hostname(self):
        """Returns the hostname of the CommServ."""
        return self._commserv_hostname

    @property
    def commserv_name(self):
        """Returns the name of the CommServ."""
        return self._commserv_name

    @property
    def commserv_timezone(self):
        """Returns the time zone of the CommServ."""
        return self._commserv_timezone

    @property
    def commserv_timezone_name(self):
        """Returns the name of the time zone of the CommServ."""
        return self._commserv_timezone_name

    @property
    def commserv_version(self):
        """Returns the version installed on the CommServ."""
        return self._commserv_version

    @property
    def webconsole_hostname(self):
        """Returns the value of the host name of the webconsole used to connect to the Commcell."""
        return self._headers['Host']

    @property
    def auth_token(self):
        """Returns the Authtoken for the current session to the Commcell."""
        return self._headers['Authtoken']

    @property
    def commcell_username(self):
        """Returns the logged in user name"""
        return self._user

    @property
    def device_id(self):
        """Returns the value of the Device ID attribute."""
        try:
            return self._device_id
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def clients(self):
        """Returns the instance of the Clients class."""
        try:
            if self._clients is None:
                self._clients = Clients(self)

            return self._clients
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def media_agents(self):
        """Returns the instance of the MediaAgents class."""
        try:
            if self._media_agents is None:
                self._media_agents = MediaAgents(self)

            return self._media_agents
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def workflows(self):
        """Returns the instance of the Workflows class."""
        try:
            if self._workflows is None:
                self._workflows = WorkFlows(self)

            return self._workflows
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def alerts(self):
        """Returns the instance of the Alerts class."""
        try:
            if self._alerts is None:
                self._alerts = Alerts(self)

            return self._alerts
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def disk_libraries(self):
        """Returns the instance of the DiskLibraries class."""
        try:
            if self._disk_libraries is None:
                self._disk_libraries = DiskLibraries(self)

            return self._disk_libraries
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def storage_policies(self):
        """Returns the instance of the StoragePolicies class."""
        return self.policies.storage_policies

    @property
    def schedule_policies(self):
        """Returns the instance of the SchedulePolicies class."""
        return self.policies.schedule_policies

    @property
    def policies(self):
        """Returns the instance of the Policies class."""
        try:
            if self._policies is None:
                self._policies = Policies(self)

            return self._policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def user_groups(self):
        """Returns the instance of the UserGroups class."""
        try:
            if self._user_groups is None:
                self._user_groups = UserGroups(self)

            return self._user_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def domains(self):
        """Returns the instance of the UserGroups class."""
        try:
            if self._domains is None:
                self._domains = Domains(self)

            return self._domains
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def client_groups(self):
        """Returns the instance of the ClientGroups class."""
        try:
            if self._client_groups is None:
                self._client_groups = ClientGroups(self)

            return self._client_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def global_filters(self):
        """Returns the instance of the GlobalFilters class."""
        try:
            if self._global_filters is None:
                self._global_filters = GlobalFilters(self)

            return self._global_filters
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def datacube(self):
        """Returns the instance of the Datacube class."""
        try:
            if self._datacube is None:
                self._datacube = Datacube(self)

            return self._datacube
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def plans(self):
        """Returns the instance of the Plans class."""
        try:
            if self._plans is None:
                self._plans = Plans(self)

            return self._plans
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def job_controller(self):
        """Returns the instance of the Jobs class."""
        try:
            if self._job_controller is None:
                self._job_controller = JobController(self)

            return self._job_controller
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def users(self):
        """Returns the instance of the Users class."""
        try:
            if self._users is None:
                self._users = Users(self)

            return self._users
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def roles(self):
        """Returns the instance of the Roles class."""
        try:
            if self._roles is None:
                self._roles = Roles(self)

            return self._roles
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def download_center(self):
        """Returns the instance of the DownloadCenter class."""
        try:
            if self._download_center is None:
                self._download_center = DownloadCenter(self)

            return self._download_center
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def organizations(self):
        """Returns the instance of the Organizations class."""
        try:
            if self._organizations is None:
                self._organizations = Organizations(self)

            return self._organizations
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def storage_pools(self):
        """Returns the instance of the StoragePools class."""
        try:
            if self._storage_pools is None:
                self._storage_pools = StoragePools(self)

            return self._storage_pools
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def monitoring_policies(self):
        """Returns the instance of the MonitoringPolicies class."""
        try:
            if self._monitoring_policies is None:
                self._monitoring_policies = MonitoringPolicies(self)

            return self._monitoring_policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def operation_window(self):
        """Returns the instance of the OperationWindow class."""
        try:
            if self._operation_window is None:
                self._operation_window = OperationWindow(self)
            return self._operation_window
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def activity_control(self):
        """Returns the instance of the ActivityControl class."""
        try:
            if self._activity_control is None:
                self._activity_control = ActivityControl(self)

            return self._activity_control
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def event_viewer(self):
        """Returns the instance of the Event Viewer class."""
        try:
            if self._events is None:
                self._events = Events(self)

            return self._events
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def array_management(self):
        """Returns the instance of the ArrayManagement class."""
        try:
            if self._array_management is None:
                self._array_management = ArrayManagement(self)

            return self._array_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def disasterrecovery(self):
        """Returns the instance of the DisasterRecovery class."""
        try:
            if self._disaster_recovery is None:
                self._disaster_recovery = DisasterRecovery(self)

            return self._disaster_recovery
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_client(self):
        """Returns the instance of the Client class for the CommServ client."""
        if self._commserv_client is None:
            self._commserv_client = self.clients.get(self._commserv_name)

        return self._commserv_client

    @property
    def commcell_migration(self):
        """Returns the instance of the CommcellMigration class"""
        try:
            if self._commcell_migration is None:
                self._commcell_migration = CommCellMigration(self)

            return self._commcell_migration
        except AttributeError:
            return  USER_LOGGED_OUT_MESSAGE

    def logout(self):
        """Logs out the user associated with the current instance."""
        if self._headers['Authtoken'] is None:
            return 'User already logged out.'

        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def request(self, request_type, request_url, request_body=None):
        """Runs the request of the type specified on the request URL, with the body passed
            in the arguments.

            Args:
                request_type    (str)   --  type of HTTP request to run on the Commcell

                    e.g.;

                        - POST

                        - GET

                        - PUT

                        - DELETE

                request_url     (str)   --  API name to run the request on with params, if any

                    e.g.;

                        - Backupset

                        - Agent

                        - Client

                        - Client/{clientId}

                        - ...

                        etc.

                request_body    (dict)  --  JSON request body to pass along with the request

                    default: None

            Returns:
                object  -   the response received from the server

        """
        request_url = self._web_service + request_url

        _, response = self._cvpysdk_object.make_request(
            request_type.upper(), request_url, request_body
        )

        return response

    def send_mail(self, receivers, subject, body=None, copy_sender=False, is_html_content=True):
        """Sends a mail to the specified email address from the email asscoiated to this user

            Args:
                receivers       (list)  --  list of email addresses to whom the email is to
                be sent

                subject         (str)   --  subject of the email that is to be sent to the user

                body            (str)   --  email body that is to be included in the email

                copy_sender     (bool)  --  copies the sender in the html report that is sent

                is_html_content (bool)  --  determines if the email body has html content

                    True    -   the email body has html content

                    False   -   the email content is plain text

            Raises:
                SDKException:
                    if failed to send an email to specified user

                    if response is empty

                    if response is not success

        """
        if body is None:
            body = ''

        send_email_request = {
            "App_SendEmailReq": {
                "emailInfo": {
                    "subject": subject,
                    "body": body,
                    "copySender": copy_sender,
                    "isHTML": is_html_content,
                    "toEmail": [
                        {
                            "emailAddress": email
                        } for email in receivers
                    ]
                }
            }
        }

        response_json = self._qoperation_execute(send_email_request)

        if response_json.get('errorCode', 0) != 0:
            raise SDKException(
                'Commcell',
                '104',
                'Error: "{}"'.format(response_json['errorMessage'])
            )

    def refresh(self):
        """Refresh the properties of the Commcell."""
        self._clients = None
        self._media_agents = None
        self._workflows = None
        self._alerts = None
        self._disk_libraries = None
        self._storage_policies = None
        self._schedule_policies = None
        self._user_groups = None
        self._domains = None
        self._client_groups = None
        self._global_filters = None
        self._datacube = None
        self._plans = None
        self._job_controller = None
        self._users = None
        self._roles = None
        self._download_center = None
        self._organizations = None
        self._policies = None
        self._storage_pools = None
        self._activity_control = None
        self._events = None
        self._monitoring_policies = None
        self._array_management = None
        self._disaster_recovery = None
        self._operation_window = None
        self._commserv_client = None
        self._commcell_migration = None
        self._get_commserv_details()

    def run_data_aging(
            self,
            copy_name=None,
            storage_policy_name=None,
            is_granular=False,
            include_all=True,
            include_all_clients=False,
            select_copies=False,
            prune_selected_copies=False,
            schedule_pattern=None):
        """
        Runs the Data Aging from Commcell,SP and copy level


        """
        if storage_policy_name is None:
            copy_name = ""
            storage_policy_name = ""

        if copy_name is None:
            copy_name = ""

        request_json = {
            "taskInfo": {
                "associations": [],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "policyType": 0,
                    "alert": {
                        "alertName": ""
                    },
                    "taskFlags": {
                        "isEdgeDrive": False,
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {

                            "subTaskType": 1,
                            "operationType": 4018
                        },

                        "options": {
                            "adminOpts": {
                                "dataAgingOption": {
                                    "selectCopies": select_copies,
                                    "includeAllClients": include_all_clients,
                                    "pruneSelectedCopies": prune_selected_copies,
                                    "isGranular": is_granular,
                                    "includeAll": include_all,
                                    "archiveGroupCopy": [
                                        {
                                            "copyName": copy_name,
                                            "storagePolicyName": storage_policy_name
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }

        if schedule_pattern:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CREATE_TASK'], request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    from .job import Job
                    return Job(self, response.json()['jobIds'][0])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Error: "{0}"'.format(error_message)
                    raise SDKException('Commcell', '105', o_str)

                elif "taskId" in response.json():
                    return Schedule(self, schedule_id=response.json()['taskId'])

                else:
                    raise SDKException('Commcell', '105')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_saml_token(self, validity=30):
        """Returns the SAML token for the currently logged-in user.

            Args:
                validity    (int)   --  validity of the SAML token, **in minutes**

                    default: 30

            Returns:
                str     -   SAML token string received from the server

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._services['GET_SAML_TOKEN'] % validity
        )

        if flag:
            if response.json():
                response = response.json()
                token = response.get('token')

                if token:
                    return token
                else:
                    error_message = response['errList'][0]['errLogMessage']
                    error_code = response['errList'][0]['errorCode']

                    raise SDKException(
                        'Commcell',
                        '106',
                        'Error Code: {0}\nError Message: {1}'.format(error_code, error_message)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_additional_setting(self, category, key_name, data_type, value):
        """Adds registry key to the commserve property.

            Args:
                category    (str)   --  Category of registry key

                key_name    (str)   --  Name of the registry key

                data_type   (str)   --  Data type of registry key

                    Accepted Values:
                        - BOOLEAN
                        - INTEGER
                        - STRING
                        - MULTISTRING
                        - ENCRYPTED

                value   (str)   --  Value of registry key

            Returns:
                None

            Raises:
                SDKException:
                    if failed to add

                    if response is empty

                    if response code is not as expected

        """
        self.commserv_client.add_additional_setting(category, key_name, data_type, value)

    def delete_additional_setting(self, category, key_name):
        """Deletes registry key from the commserve property.

            Args:
                category    (str)   --  Category of registry key

                key_name    (str)   --  Name of the registry key

            Returns:
                None

            Raises:
                SDKException:
                    if failed to delete

                    if response is empty

                    if response code is not as expected

        """
        self.commserv_client.delete_additional_setting(category, key_name)

    def protected_vms(self, days):
        """
        Returns all the protected VMs for the particular client for passed days
        Args:
            days: Protected VMs for days
                ex: if value is 30 , returns VM prtected in past 30 days

        Returns:
                vm_dict -  all properties of VM prtotected for passed days

        """

        from_time, to_time = self._convert_days_to_epoch(days)
        self._PROTECTED_VMS = self._services['PROTECTED_VMS'] % (from_time, to_time)
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._PROTECTED_VMS
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))
