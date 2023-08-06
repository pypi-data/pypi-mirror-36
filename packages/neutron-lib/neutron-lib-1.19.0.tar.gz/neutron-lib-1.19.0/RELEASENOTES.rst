===========
neutron-lib
===========

.. _neutron-lib_1.19.0:

1.19.0
======

.. _neutron-lib_1.19.0_New Features:

New Features
------------

.. releasenotes/notes/add-is-default-to-network-d16a2e6bcfae943a.yaml @ b'7fa92e37b47641e26c071fb03d3d042e0e1bb0aa'

- The ``project-default-networks`` extension is now available and adds a new
  attribute ``project_default`` into the ``network`` resource.
  This attribute will be used to indicate if a network is a project
  default network.

.. releasenotes/notes/gateway-ip-qos-ext-d3ffb5f517c9f713.yaml @ b'7124d76e77e9a07c4e838c7dfd7ec9242ca19d0c'

- Add new extension `qos-gateway-ip` which extends the `router_gw_info`
  with new attribute `qos_policy_id`.

.. releasenotes/notes/mac-generator-f927df2fe57300c0.yaml @ b'b8677baeb70c53780dcbf9b363c1a4a83d1561fd'

- Introduced ``neutron_lib.utils.net.random_mac_generator(basemac)``. It allows
  you to get a mac address string Python generator from the same kind of
  basemac that ``neutron_lib.utils.net.get_random_mac(basemac)`` expects. If
  there are a lot of macs to get, this will speed the process up
  significantly over generating single macs and testing for collisions.

.. releasenotes/notes/placement-client-update-ensure-rp-9e5c3cf34d49b212.yaml @ b'203f4f06961481e4013dd11c0e74afb9ffe354a4'

- New methods available in Placement client:
  ``update_resource_provider`` and ``ensure_resource_provider``.

.. releasenotes/notes/placement-constants-f2629b98f6fe148f.yaml @ b'b271a336b13c0d8d6b5ef0078412d87040094747'

- New constants module for Placement: ``neutron_lib.placement.constants``.

.. releasenotes/notes/placement-utils-a66e6b302d2bc8f0.yaml @ b'579e0ccabbd5ec132366fe51f46be653cbf15986'

- neutron-lib now has a new module: ``neutron_lib.placement.utils``.
  This module contains logic that is to be shared between in-tree
  Neutron components and possibly out-of-tree Neutron agents that want
  to support features involving the Placement service (for example
  guaranteed minimum bandwidth).

.. releasenotes/notes/policy-in-code-1e73cabebd41d66e.yaml @ b'bede7826300884fba1a64aae3b807ccbb419b5ca'

- policy-in-code support in neutron-lib is added.
  The default policies for 'context_is_admin' and 'context_is_advsvc' are
  now implemented as embeded policies.
  (Note that the main policy-in-code support will be implemented
  in the main neutron codebase.)

.. releasenotes/notes/port-resource-request-cb520720cd19523b.yaml @ b'061a77b4f2d2c8c000b475ee034841a6096c9465'

- The new extension ``port-resource-request`` adds the ``resource_request`` attribute to port responses. This attribute enables Neutron to communicate to Nova resources needed by the port, such as physnet, VNIC type and bandwidth. If the port requested by Nova boot has the ``resource_request`` attribute, then the Nova Scheduler will try to allocate the VM in a host that can satisfy those requirements.

.. releasenotes/notes/qos-bw-minimum-ingress-cff397e598b6fa3a.yaml @ b'e77c9befd4677c847a6afff4cb164b02cceb9352'

- New extension ``qos-bw-minimum-ingress`` for extending ``qos_minimum_bandwidth_rule`` with ingress direction for placement based enforcement.

.. releasenotes/notes/resource-provider-uuid5-namespace-f7276ba1945ce82f.yaml @ b'c2e205b85a08bd0cea79e566883362e0b60d9728'

- New MechanismDriver API class property:
  ``resource_provider_uuid5_namespace``.  Mechanism drivers wanting
  to support resource provider information reporting to Placement
  (eg. reporting resource providers to guarantee some minimum bandwidth
  allocated on them later) must set this class property to a UUID
  object unique to that mechanism driver. It will be used as a UUID
  v5 namespace in generating UUIDs for resource providers. The default
  implementation sets it to ``None``, meaning that the mechanism driver
  does not support resource provider information reporting to Placement.
  Unaffected drivers need not be changed.

.. releasenotes/notes/responsible_for_ports_allocation-5599dc59b3c98db2.yaml @ b'679481f374c969d4887fe686f342dd04ab918b62'

- New MechanismDriver API method: ``responsible_for_ports_allocation``.
  Mechanism drivers wanting to support resource allocations for ports in
  Placement (eg. wanting to guarantee some minimum bandwidth allocated
  on the resource provider in the port's ``binding:profile.allocation``)
  must implement this method. The default implementation reports not
  being responsible for any resource providers, therefore unaffected
  drivers need not be changed.


.. _neutron-lib_1.19.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/reset-db-retry-settings-49e51cef4c842f69.yaml @ b'ed62a06a536a39b1236bd4dcadb2dd13cc2c4b4b'

- Increase the DB retry interval and max retry times for the
  ``retry_db_errors`` decorator in ``neutron_lib.db.api`` to
  0.5 seconds and 20 times, respectively. For those actions
  which have a higher chance for DBDeadlock, users should have
  a higher success rate due to the larger random range and retry
  times. For more information
  see bug `1777968 <https://bugs.launchpad.net/neutron/+bug/1777968>`_


.. _neutron-lib_1.19.0_Other Notes:

Other Notes
-----------

.. releasenotes/notes/add-two-fields-to-duplicated-entry-exception-75b0e07c6e1cc6ae.yaml @ b'd47549344e353f4ba3e16effb7fd8e2ec4dca3bb'

- Add two fields ``columns`` and ``value`` to exception
  ``NeutronDbObjectDuplicateEntry``. These two fields are populated
  from the corresponding db exception.

.. releasenotes/notes/placement-client-bump-latest-supported-version-to-1-20-fe96751dab42399b.yaml @ b'0555ffe4b2f5f6dad8380aa4d79129caa09cdac1'

- Bump ``PlacementAPIClient's`` max supported microversion to ``1.20``,
  as from that microversion placement API returns json body for
  POST /resource_providers.

.. releasenotes/notes/placement-client-move-9f292ae2067c119c.yaml @ b'd32e570361a636531a2a143fdf004a81e3e28894'

- The ``PlacementAPIClient`` class is moved from
  ``neutron_lib.clients.placement`` to ``neutron_lib.placement.client``
  in order to consolidate all Placement related logic under sub-package
  ``neutron_lib.placement``.

.. releasenotes/notes/placement-client-optional-rp-generations-44d1f1055d5496be.yaml @ b'74c62da3b5076015563b9f8fe269818546db66cb'

- The ``resource_provider_generation`` parameters of the following
  methods of ``PlacementAPIClient`` are now optional:
  ``update_resource_provider_inventories``,
  ``update_resource_provider_inventory`` and
  ``update_resource_provider_traits``.
  You may call the methods without this parameter or pass ``None``
  with the meaning to ignore resource provider generations. That is the
  client will (in quick succession) get the object and update it supplying
  the same generation.

.. releasenotes/notes/placement-client-return-f4f22d244e7b174a.yaml @ b'5aa28473673405d4c70e518fb1f46b8b55fba51d'

- The ``create_resource_provider`` and ``associate_aggregates``
  methods of ``PlacementAPIClient`` now return the parsed
  body of the respective responses. Since these methods returned ``None``
  previously this is unlikely to break anything. On the other hand callers
  of these methods now have a chance to simplify their code.

.. releasenotes/notes/update-segment-api-definition-d7297e73e76a754c.yaml @ b'e3d90fef655b41c36f0e6401a3b19118d496d99c'

- This release removes the ``description`` from the segment extension's
  attribute map as well as adds the ``standard-attr-description`` as
  required dependency and ``standard-attr-segment`` as an optional
  dependency.

