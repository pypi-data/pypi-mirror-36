from __future__ import absolute_import, unicode_literals

from c8.utils import get_col_name

__all__ = ['Tenant']

from datetime import datetime

from c8.api import APIWrapper
from c8.request import Request
from c8.executor import (
    DefaultExecutor,
    AsyncExecutor,
    BatchExecutor,
    TransactionExecutor,
)

from c8.exceptions import (
    TenantDeleteError,
    TenantCreateError,
    TenantListError,
    TenantDcListError,
    TenantPropertiesError,
    StreamCreateError,
    StreamDeleteError,
    StreamListError,
    StreamPropertiesError,
    StreamStatisticsError,
    StreamConnectionError,
    PermissionListError,
    PermissionGetError,
    PermissionResetError,
    PermissionUpdateError,
    ServerConnectionError,
    ServerDetailsError,
    ServerVersionError,
    UserCreateError,
    UserDeleteError,
    UserGetError,
    UserListError,
    UserReplaceError,
    UserUpdateError,
)



class Tenant(APIWrapper):
    """Base class for Tenant API wrappers.

    :param connection: HTTP connection.
    :type connection: c8.connection.Connection
    :param executor: API executor.
    :type executor: c8.executor.Executor
    """

    def __init__(self, connection):
        super(Tenant, self).__init__(connection, executor=DefaultExecutor(connection))

    @property
    def name(self):
        """Return tenant name.

        :return: tenant name.
        :rtype: str | unicode
        """
        return self.tenant_name

    #######################
    # Tenant Management #
    #######################

    def tenants(self):
        """Return the names all tenants.

        :return: Tenant names.
        :rtype: [str | unicode]
        :raise c8.exceptions.TenantListError: If retrieval fails.
        """
        request = Request(
            method='get',
            endpoint='/_api/tenants'
        )

        def response_handler(resp):
            if not resp.is_success:
                raise TenantListError(resp, request)
            #print("tenants() : Response body: " + str(resp.body))
            retval = []
            for item in resp.body['result']:
                retval.append(item['tenant'])
            return retval

        return self._execute(request, response_handler)

    def has_tenant(self, name):
        """Check if a tenant exists.

        :param name: Tenant name.
        :type name: str | unicode
        :return: True if tenant exists, False otherwise.
        :rtype: bool
        """
        return name in self.tenants()

    def create_tenant(self, name, passwd='', extra={}):
        """Create a new tenant.
        :param name: Tenant name.
        :type name: str | unicode
        :param passwd: What I presume is the tenant admin user password.
        :param extra: Extra config info.
        :type extra: [dict]
        :return: True if tenant was created successfully.
        :rtype: bool
        :raise c8.exceptions.TenantCreateError: If create fails.

        Here is an example entry for parameter **users**:

        .. code-block:: python

            {
                'username': 'john',
                'password': 'password',
                'active': True,
                'extra': {'Department': 'IT'}
            }
        """
        data = {'name': name}
        data['passwd'] = passwd
        data['extra'] = extra

        request = Request(
            method='post',
            endpoint='/_api/tenant',
            data=data
        )

        def response_handler(resp):
            if not resp.is_success:
                raise TenantCreateError(resp, request)
            return True

        return self._execute(request, response_handler)
    
    def update_tenant(self, name, passwd='', extra={}):
        """Update a existing tenant.
        :param name: Tenant name.
        :type name: str | unicode
        :param passwd: What I presume is the tenant admin user password.
        :param extra: Extra config info.
        :type extra: [dict]
        :return: True if tenant was created successfully.
        :rtype: bool
        :raise c8.exceptions.TenantCreateError: If create fails.

        Here is an example entry for parameter **users**:

        .. code-block:: python

            {
                'username': 'john',
                'password': 'password',
                'active': True,
                'extra': {'Department': 'IT'}
            }
        """
        data = {'name': name}
        data['passwd'] = passwd
        data['extra'] = extra

        request = Request(
            method='patch',
            endpoint='/_api/tenant/{tenantname}'.format(tenantname=name),
            data=data
        )

        def response_handler(resp):
            if not resp.is_success:
                raise TenantUpdateError(resp, request)
            return True

        return self._execute(request, response_handler)

    def delete_tenant(self, name, ignore_missing=False):
        """Delete the tenant.
        :param name: Tenant name.
        :type name: str | unicode
        :param ignore_missing: Do not raise an exception on missing tenant.
        :type ignore_missing: bool
        :return: True if tenant was deleted successfully, False if tenant
            was not found and **ignore_missing** was set to True.
        :rtype: bool
        :raise c8.exceptions.TenantDeleteError: If delete fails.
        """
        request = Request(
            method='delete',
            endpoint='/_api/tenant/{tenantname}'.format(tenantname=name)
        )

        def response_handler(resp):
            #print("DELETE TENANT: RESP BODY IS: "+str(resp.body)) # TODO REMOVE FROM PRODUCTION
            if resp.error_code == 1228 and ignore_missing:
                return False
            if not resp.is_success:
                raise TenantDeleteError(resp, request)
            return resp.body['result']

        return self._execute(request, response_handler)


    def dclist(self):
        """Return the list of Datacenters

        :return: DC List.
        :rtype: [str | unicode ]
        :raise c8.exceptions.TenantListError: If retrieval fails.
        """
        request = Request(
            method='get',
            endpoint='/_api/datacenter/all'
        )

        def response_handler(resp):
            #print("dclist() : Response body: " + str(resp.body))
            if not resp.is_success:
                raise TenantDcListError(resp, request)
            dc_list = []
            for dc in resp.body:
                dc_list.append(dc['name'])
            return dc_list

        return self._execute(request, response_handler)

    def dclist_local(self):
        """Return the list of local Datacenters

        :return: DC List.
        :rtype: [str | unicode ]
        :raise c8.exceptions.TenantListError: If retrieval fails.
        """
        request = Request(
            method='get',
            endpoint='/_api/datacenter/local'
        )

        def response_handler(resp):
            #print("dclist() : Response body: " + str(resp.body))
            if not resp.is_success:
                raise TenantDcListError(resp, request)
            return resp.body

        return self._execute(request, response_handler)

    ###################
    # Streams Management
    ###################
    ## TODO

    # def streams(self):
    #     """Return the names of all streams for this tenant .

    #     :return: stream names.
    #     :rtype: [str | unicode]
    #     :raise c8.exceptions.TenantListError: If retrieval fails.
    #     """
    #     request = Request(
    #         method='get',
    #         endpoint='/c8/_tenant/<tenant-name>/streams' # sample
    #     )

    #     def response_handler(resp):
    #         if not resp.is_success:
    #             raise TenantListError(resp, request)
    #         return resp.body['result']

    #     return self._execute(request, response_handler)

    # def has_stream(self, name):
    #     """Check if a stream exists.

    #     :param name: stream name.
    #     :type name: str | unicode
    #     :return: True if stream exists, False otherwise.
    #     :rtype: bool
    #     """
    #     return name in self.streams()

    # def create_stream(self, name, dclist=[], policies=None):
    #     """Create a new stream.

    #     :param name: stream name.
    #     :type name: str | unicode
    #     :param dclist: List of data centers to replicate the stream.
    #     :type dclist: [string]
    #     :param policies: List of policies to apply to the stream.
    #     :type policies: [policy]
    #     :return: True if stream was created successfully.
    #     :rtype: bool
    #     :raise c8.exceptions.StreamCreateError: If create fails.

    #     Here is an example entry for parameter **users**:

    #     .. code-block:: python

    #         {
    #             'name': 'alert-stream',
    #             'dclist': ['dc1','dc2']
    #         }
    #     """
    #     request = Request(
    #         method='post',
    #         endpoint='/c8/_tenant/<tenant-name>/streams/<stream-name>',  # sample
    #         data=dclist
    #     )

    #     def response_handler(resp):
    #         if not resp.is_success:
    #             raise StreamCreateError(resp, request)
    #         return True

    #     return self._execute(request, response_handler)

    # def delete_stream(self, name, ignore_missing=False):
    #     """Delete the Stream and all topics under the stream

    #     :param name: Stream name.
    #     :type name: str | unicode
    #     :param ignore_missing: Do not raise an exception on missing stream.
    #     :type ignore_missing: bool
    #     :return: True if stream was deleted successfully, False if stream
    #         was not found and **ignore_missing** was set to True.
    #     :rtype: bool
    #     :raise c8.exceptions.StreamDeleteError: If delete fails.
    #     """
    #     request = Request(
    #         method='delete',
    #         endpoint='/c8/_tenant/<tenant-name>/streams/<stream-name>{}'.format(name) # sample
    #     )

    #     def response_handler(resp):
    #         if resp.error_code == 1228 and ignore_missing:
    #             return False
    #         if not resp.is_success:
    #             raise StreamDeleteError(resp, request)
    #         return resp.body['result']

    #     return self._execute(request, response_handler)

    ###################
    # User Management #
    ###################

    def has_user(self, username):
        """Check if user exists.

        :param username: Username.
        :type username: str | unicode
        :return: True if user exists, False otherwise.
        :rtype: bool
        """
        return any(user['username'] == username for user in self.users())

    def users(self):
        """Return all user details.

        :return: List of user details.
        :rtype: [dict]
        :raise c8.exceptions.UserListError: If retrieval fails.
        """
        request = Request(
            method='get',
            endpoint='/_admin/user'
        )

        def response_handler(resp):
            #print("TENANT USERS RESP BODY: "+str(resp.body))
            if not resp.is_success:
                raise UserListError(resp, request)
            return [{
                'username': record['user'],
                'active': record['active'],
                'extra': record['extra'],
            } for record in resp.body['result']]

        return self._execute(request, response_handler)

    def user(self, username):
        """Return user details.

        :param username: Username.
        :type username: str | unicode
        :return: User details.
        :rtype: dict
        :raise c8.exceptions.UserGetError: If retrieval fails.
        """
        request = Request(
            method='get',
            endpoint='/_admin/user/{}'.format(username)
        )

        def response_handler(resp):
            #print("TENANT USER DETAILS RESP BODY: "+str(resp.body))
            if not resp.is_success:
                raise UserGetError(resp, request)
            return {
                'username': resp.body['user'],
                'active': resp.body['active'],
                'extra': resp.body['extra']
            }

        return self._execute(request, response_handler)

    def create_user(self, username, password, active=True, extra=None):
        """Create a new user.

        :param username: Username.
        :type username: str | unicode
        :param password: Password.
        :type password: str | unicode
        :param active: True if user is active, False otherwise.
        :type active: bool
        :param extra: Additional data for the user.
        :type extra: dict
        :return: New user details.
        :rtype: dict
        :raise c8.exceptions.UserCreateError: If create fails.
        """
        data = {'user': username, 'passwd': password, 'active': active}
        if extra is not None:
            data['extra'] = extra

        request = Request(
            method='post',
            endpoint='/_admin/user',
            data=data
        )

        def response_handler(resp):
            if not resp.is_success:
                raise UserCreateError(resp, request)
            return {
                'username': resp.body['user'],
                'active': resp.body['active'],
                'extra': resp.body['extra'],
            }

        return self._execute(request, response_handler)

    def update_user(self, username, password=None, active=None, extra=None):
        """Update a user.

        :param username: Username.
        :type username: str | unicode
        :param password: New password.
        :type password: str | unicode
        :param active: Whether the user is active.
        :type active: bool
        :param extra: Additional data for the user.
        :type extra: dict
        :return: New user details.
        :rtype: dict
        :raise c8.exceptions.UserUpdateError: If update fails.
        """
        data = {}
        if password is not None:
            data['passwd'] = password
        if active is not None:
            data['active'] = active
        if extra is not None:
            data['extra'] = extra

        request = Request(
            method='patch',
            endpoint='/_admin/user/{user}'.format(user=username),
            data=data
        )

        def response_handler(resp):
            if not resp.is_success:
                raise UserUpdateError(resp, request)
            return {
                'username': resp.body['user'],
                'active': resp.body['active'],
                'extra': resp.body['extra'],
            }

        return self._execute(request, response_handler)

    def replace_user(self, username, password, active=None, extra=None):
        """Replace a user.

        :param username: Username.
        :type username: str | unicode
        :param password: New password.
        :type password: str | unicode
        :param active: Whether the user is active.
        :type active: bool
        :param extra: Additional data for the user.
        :type extra: dict
        :return: New user details.
        :rtype: dict
        :raise c8.exceptions.UserReplaceError: If replace fails.
        """
        data = {'user': username, 'passwd': password}
        if active is not None:
            data['active'] = active
        if extra is not None:
            data['extra'] = extra

        request = Request(
            method='put',
            endpoint='/_admin/user/{user}'.format(user=username),
            data=data
        )

        def response_handler(resp):
            if resp.is_success:
                return {
                    'username': resp.body['user'],
                    'active': resp.body['active'],
                    'extra': resp.body['extra'],
                }
            raise UserReplaceError(resp, request)

        return self._execute(request, response_handler)

    def delete_user(self, username, ignore_missing=False):
        """Delete a user.

        :param username: Username.
        :type username: str | unicode
        :param ignore_missing: Do not raise an exception on missing user.
        :type ignore_missing: bool
        :return: True if user was deleted successfully, False if user was not
            found and **ignore_missing** was set to True.
        :rtype: bool
        :raise c8.exceptions.UserDeleteError: If delete fails.
        """
        request = Request(
            method='delete',
            endpoint='/_admin/user/{user}'.format(user=username)
        )

        def response_handler(resp):
            if resp.is_success:
                return True
            elif resp.status_code == 404 and ignore_missing:
                return False
            raise UserDeleteError(resp, request)

        return self._execute(request, response_handler)

    #########################
    # Permission Management #
    #########################

    def permissions(self, username):
        """Return user permissions for all databases and collections.

        :param username: Username.
        :type username: str | unicode
        :return: User permissions for all databases and collections.
        :rtype: dict
        :raise: c8.exceptions.PermissionListError: If retrieval fails.
        """
        request = Request(
            method='get',
            endpoint='/_admin/user/{}/database'.format(username),
            params={'full': True}
        )

        def response_handler(resp):
            if resp.is_success:
                return resp.body['result']
            raise PermissionListError(resp, request)

        return self._execute(request, response_handler)

    def permission(self, username, database, collection=None):
        """Return user permission for a specific database or collection.

        :param username: Username.
        :type username: str | unicode
        :param database: database name.
        :type database: str | unicode
        :param collection: Collection name.
        :type collection: str | unicode
        :return: Permission for given database or collection.
        :rtype: str | unicode
        :raise: c8.exceptions.PermissionGetError: If retrieval fails.
        """
        endpoint = '/_admin/user/{}/database/{}'.format(username, database)
        if collection is not None:
            endpoint += '/' + collection
        request = Request(method='get', endpoint=endpoint)

        def response_handler(resp):
            if not resp.is_success:
                raise PermissionGetError(resp, request)
            return resp.body['result']

        return self._execute(request, response_handler)

    def update_permission(self,
                          username,
                          permission,
                          database,
                          collection=None):
        """Update user permission for a specific database or collection.

        :param username: Username.
        :type username: str | unicode
        :param database: database name.
        :type database: str | unicode
        :param collection: Collection name.
        :type collection: str | unicode
        :param permission: Allowed values are "rw" (read and write), "ro"
            (read only) or "none" (no access).
        :type permission: str | unicode
        :return: True if access was granted successfully.
        :rtype: bool
        :raise c8.exceptions.PermissionUpdateError: If update fails.
        """
        endpoint = '/_admin/user/{}/database/{}'.format(username, database)
        if collection is not None:
            endpoint += '/' + collection

        request = Request(
            method='put',
            endpoint=endpoint,
            data={'grant': permission}
        )

        def response_handler(resp):
            if resp.is_success:
                return True
            raise PermissionUpdateError(resp, request)

        return self._execute(request, response_handler)

    def reset_permission(self, username, database, collection=None):
        """Reset user permission for a specific database or collection.

        :param username: Username.
        :type username: str | unicode
        :param database: database name.
        :type database: str | unicode
        :param collection: Collection name.
        :type collection: str | unicode
        :return: True if permission was reset successfully.
        :rtype: bool
        :raise c8.exceptions.PermissionRestError: If reset fails.
        """
        endpoint = '/_admin/user/{}/database/{}'.format(username, database)
        if collection is not None:
            endpoint += '/' + collection

        request = Request(method='delete', endpoint=endpoint)

        def response_handler(resp):
            if resp.is_success:
                return True
            raise PermissionResetError(resp, request)

        return self._execute(request, response_handler)
