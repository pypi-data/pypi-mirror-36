=================
diskimage-builder
=================

.. _diskimage-builder_2.17.0:

2.17.0
======

.. _diskimage-builder_2.17.0_Other Notes:

Other Notes
-----------

.. releasenotes/notes/bootloader-commandline-d2db7524f1f9ad28.yaml @ f6a2452d4c72d52af1abd6f9d4165ff19a0506ba

- It has been clarified that the ``DIB_BOOTLOADER_DEFAULT_CMDLINE`` variable appends its values to grubs ``GRUB_CMDLINE_LINUX_DEFAULT``, which is used during all normal boots but not rescue boots; as opposed to applying to ``GRUB_CMDLINE_LINUX``


.. _diskimage-builder_2.16.0:

2.16.0
======

.. _diskimage-builder_2.16.0_New Features:

New Features
------------

.. releasenotes/notes/add-modprobe-element-8e3b0287ebb11920.yaml @ 31383970c72cd96e9b69c7e4a9e5a92bf9f72529

- Add new modprobe element. This element will replace modprobe-blacklist element. It wil still have the blacklist functionality, but it also adds the feature of passing a complete file with settings to the modprobe.d directory. Adding this functionality, that will allow elements that depends on this module, to just copy the specified files to the final directory.


.. _diskimage-builder_2.16.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/ubuntu-arbitrary-images-c796f5c6dbd40679.yaml @ fde82c1f192d346ac3992b1ba30935d29f29818b

- You would need to modify your ``DIB_CLOUD_IMAGES`` and possibly
  ``SHA256SUMS`` variables if you were using them to build Ubuntu with
  elements/ubuntu: ``DIB_CLOUD_IMAGES`` would need to contain URL with
  path, and ``SHA256SUMS`` would not now neccesarily point to
  ``$DIB_RELEASE/current/`` directory.


.. _diskimage-builder_2.12.0:

2.12.0
======

.. _diskimage-builder_2.12.0_New Features:

New Features
------------

.. releasenotes/notes/bootloader-gpt-d1047f81f3a0631b.yaml @ 55b479b54f8cd064144ba8d1e2e5be33b6a975c8

- GPT support is added to the bootloader; see documentation for
  configuration examples.  This should be considered a technology
  preview; there may be minor behaviour modifications as we enable
  UEFI and support across more architectures.


.. _diskimage-builder_2.11.0:

2.11.0
======

.. _diskimage-builder_2.11.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/incorrect-grub-label-5d2000215c0cc73e.yaml @ c7da8bc90aa9dd917ee9a4ae6b6e6cef8a9825d6

- This fixes bug 1742170 where the grub root label is different than the
  file system label when booting from a whole disk image.

.. releasenotes/notes/upgrade-pip-before-c-d2443847f9d58c7a.yaml @ 34ff72f2530ed8925c8b5d71371808d39986866f

- This fixes bug 1744403 where 60-ironic-agent-install fails to run
  when DIB_INSTALLTYPE_ironic_agent=source is set.  pip installs
  constraints with the -c argument and this argument is a relatively
  newer addion.  The currently installed pip may not support that
  option and must be upgraded before proceeding.


.. _diskimage-builder_2.10.0:

2.10.0
======

.. _diskimage-builder_2.10.0_New Features:

New Features
------------

.. releasenotes/notes/sysprep-f3fd036bc1d2c405.yaml @ 6c2b1465cce11631f5d6bf757ea194b26ca3cb7f

- Adds sysprep element included by all systemd distros

.. releasenotes/notes/timestamp-43015aa5434e8ddb.yaml @ f60dd384827beb8ec193ac7738e973941fc8b6d5

- A ``--logfile`` option is added to save output to a given file.

.. releasenotes/notes/timestamp-43015aa5434e8ddb.yaml @ f60dd384827beb8ec193ac7738e973941fc8b6d5

- By default, all ``stdout`` will log with timestamps (this used to be inconsistent; python tools logged with a timestamp, and bash parts did not).  If you set ``DIB_NO_TIMESTAMP`` to ``1`` the timestamp prefix will be suppressed (this would be appropriate if you are running diskimage-builder and capturing its output, and adding your own timestamp).  Note that output to ``--logfile`` will always be timestamped.

.. releasenotes/notes/timestamp-43015aa5434e8ddb.yaml @ f60dd384827beb8ec193ac7738e973941fc8b6d5

- You can set ``DIB_QUIET`` to ``1`` to suppress all output.  This is likely only useful when used with the ``--logfile`` command.


.. _diskimage-builder_2.10.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/sysprep-f3fd036bc1d2c405.yaml @ 6c2b1465cce11631f5d6bf757ea194b26ca3cb7f

- Adds default sysprep element clearing /etc/machine-id which
  prevents duplicated /etc/machine-id by forcing systemd to
  generate a new id for each booted system.


.. _diskimage-builder_2.9.0:

2.9.0
=====

.. _diskimage-builder_2.9.0_New Features:

New Features
------------

.. releasenotes/notes/block-device-lvm-c3b8a214952b4db5.yaml @ c2dc3dc78e52c399a30035ac00cf6c3e9effeb23

- Adds lvm support, allowing to create volumes.


.. _diskimage-builder_2.9.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/fedora26-690b9fd9ac3c3d4f.yaml @ 7cbbee7ea347cac690b6aabe98c2f220e374ad86

- The ``fedora-minimal`` and ``fedora`` elements have been updated to default to Fedora 26.  Note if you to pin to specific versions, be sure to specify ``DIB_RELEASE``.


.. _diskimage-builder_2.8.0:

2.8.0
=====

.. _diskimage-builder_2.8.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/opensuse-423-default-3bc73fff69374cd0.yaml @ 1c4c4fd7349bd78937c237dfe13fa3891945eff1

- The opensuse and opensuse-minimal element are now defaulting to 42.3, which
  is the latest stable openSUSE release. Building for 42.2 is still supported,
  however requires setting DIB_RELEASE to '42.2' explicitly.


.. _diskimage-builder_2.7.0:

2.7.0
=====

.. _diskimage-builder_2.7.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/centos-retired-f17ae9f6f03e57e3.yaml @ a00d02f6a1573ee8257105ebc18bcaba92e78ff8

- The ``centos`` and ``rhel`` elements have been removed.  These
  were building version 6 which is no longer supported (mostly due
  to a lack of python 2.7).  Version 7 support is available via the
  ``centos7`` and ``rhel7`` elements (which downloads and modifies
  the upstream cloud images) or via ``centos-minimal`` (which builds
  the image from a empty chroot; only available for CentOS).
  ``centos-minimal`` is suggested as this is what OpenStack
  Infrastructure uses for its elements.
  
  Unfortunately, ``centos-minimal`` sets ``DISTRO=centos`` while
  ``centos7`` sets ``DISTRO=centos7``, despite building the same
  thing as far as upper levels are concerned.  We plan to rectify
  this in the version 8 time-frame.

.. releasenotes/notes/dib-distribution-mirror-8c241c0d3d4a539a.yaml @ 3457d2f8e82ee936ffe227e71379b437f9632a1c

- The ``DIB_[DISTRO]_DISTRIBUTION_MIRROR`` variables have been removed.  These were undocumented ways to set ``DIB_DISTRIBUTION_MIRROR`` for some elements.  It was not implemented consistently and causing some confusion.  If you need to setup mirrors for testing purposes, the ``openstack-ci-mirrors`` element is a good example that is used by OpenStack gate testing.


.. _diskimage-builder_2.6.0:

2.6.0
=====

.. _diskimage-builder_2.6.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/dracut-network-adaabf90da9f6866.yaml @ 54765fd2f43e43d5b2dc25e8b4cff598e9095327

- The ``dracut-network`` element has been removed.  It has not been functioning for some time due to incorrect paths.


.. _diskimage-builder_2.4.0:

2.4.0
=====

.. _diskimage-builder_2.4.0_New Features:

New Features
------------

.. releasenotes/notes/block-device-mkfs-mount-fstab-42d7efe28fc2df04.yaml @ e4e23897a13a3f3b9d28cc8d288990ab0fcc5b92

- Adds mkfs, mount and fstab to the block device layer.


.. _diskimage-builder_2.3.0:

2.3.0
=====

.. _diskimage-builder_2.3.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/dib-run-parts-6f67d038aa5a4156.yaml @ 6802cf7100e01527fcf88860e65f613f0af3e244

- The ``dib-run-parts`` element is no longer required as
  ``disk-image-create`` will directly source the internal version
  for running scripts within the chroot.  This element was
  unintentionally leaving ``/usr/local/bin/dib-run-parts`` in the
  built image.  From code search we do not believe anyone was
  relying on the presence of this script.  If you do require it, you
  should source the ``dib-utils`` package to install.

.. releasenotes/notes/dib-run-parts-e18cc3a6c2d66c24.yaml @ fd424757a64921a60b92837a625a23b8f681130a

- dib no longer exports ``dib-run-parts``.  Adding this was an
  oversight made during v2 development, since ``dib-utils`` already
  provides this.  The ``dib-run-parts`` used internally
  (``diskimage_builder/lib/dib-run-parts``) is not intended to be
  used by external tools.  If you require ``dib-run-parts``, you
  should install the ``dib-utils`` package.


.. _diskimage-builder_2.3.0_Other Notes:

Other Notes
-----------

.. releasenotes/notes/dash-p-after-install-58a87549c1c906c3.yaml @ 95503b42017a3b96f810e3195d8edaa64995ce78

- The packages specified with the `-p` command-line operation are now installed after the `install.d` phase, not before.  This is to give elements priority when installing packages.  The flag documentation has been updated to describe this.


.. _diskimage-builder_2.1.0:

2.1.0
=====

.. _diskimage-builder_2.1.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/dib-init-system_fix_for_debian_jessie-c6f7261ee84dad27.yaml @ 20389d755f60b1be43a819df8a8c80e4f6cd37ef

- dib-init-system did not correctly find the init system for Debian Jessie and Debian Stretch. This version also looks for /bin/systemctl as as hint for systemd and fixes the problem.


.. _diskimage-builder_2.0.0:

2.0.0
=====

.. _diskimage-builder_2.0.0_Prelude:

Prelude
-------

.. releasenotes/notes/dibv2-omnibus-b30e0c7ecd76db8d.yaml @ 6887e796e10b57b55ee01965b48e6e698cede520

Version 2.0.0 of diskimage-builder incorporates recent work from the feature/v2 branch.  This includes incorporating some largely internal changes to the way it finds and calls elements, enhancements to partitioning and removal of some long-deprecated elements.
If you use dib exclusively via the command-line disk-image-create installed from a package or via pypi you are unlikely to notice any difference (if you run it directly from a git-tree checkout, you may be affected).

.. _diskimage-builder_2.0.0_New Features:

New Features
------------

.. releasenotes/notes/dibv2-omnibus-b30e0c7ecd76db8d.yaml @ 6887e796e10b57b55ee01965b48e6e698cede520

- 2.0.0 includes a new framework for partitioning contributed by
  Andreas Florath.  This should allow for creating multiple
  partitions, images with encryption, LVM support and flexibility
  for multiple-devices, all of which are currently not supported.
  Please check the v2 documentation, specs and reach out if these
  features interest you (some parts still in review).

.. releasenotes/notes/dibv2-omnibus-b30e0c7ecd76db8d.yaml @ 6887e796e10b57b55ee01965b48e6e698cede520

- Element override is now supported.  If you have an element of the
  same name earlier in the ``ELEMENTS_PATH``, it will override later
  instances (previously, the behaviour was undefined).


.. _diskimage-builder_2.0.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/dibv2-omnibus-b30e0c7ecd76db8d.yaml @ 6887e796e10b57b55ee01965b48e6e698cede520

- For purposes of both users and development we want dib to be as
  "pythonic" as possible and behave like all other projects.  Two
  major visible changes are:
  
  - command-line scripts are entry points (i.e. need to be installed)
  - elements have moved under diskimage_create module
  
  The result of the first is that ``./bin/disk-image-create`` from
  the source tree is no longer there.  Like all other projects, you
  should install dib into a virtualenv (if you're developing, use
  pip -e) and ``disk-image-create`` will "just work".
  
  The second change, moving the inbuilt elements under the
  ``diskimage_create`` module, is a simplification so we always have
  a canonical path to our elements.  Since we now always know where
  elements are relative to the imported diskimage_builder module we
  can drop all the path guessing complexity.  This has other good
  flow-on effects such as ``testr`` being able to find unit-tests
  for elements in the normal fashion and having imports work as
  usual.
  
  We are aware there are a number of tools that like to take dib
  elements and do things with them. Reading some of the dib source
  you may find there is a canonical way to find out the included dib
  elements path -- ask dib itself, something like
  
  .. code-block:: shell
  
     DIB_ELEMENTS=$(python -c '
     import diskimage_builder.paths;
     diskimage_builder.paths.show_path("elements")')
  
  Note you probably do not want this.  As mentioned, another feature
  of v2 is override elements -- an element that appears first in the
  element path-list will override any built-in one (just like
  $PATH).  There is a function,
  ``diskimage_builder.get_elements()``, which will correctly process
  the element path, calculate overrides and return a canonical list
  of elements, their dependencies and correct paths.
  
  *That* said, you probably do not want this either!  There are a
  number of elements that do things on behalf of other elements --
  they look for a file in the included elements, say, and use that
  as a manifest for something.  Previously, these would just have to
  make up their own element processing via inspection of the
  command-line arguments.  dib now exports pre-computed variables
  that an element can walk for all the current build elements -- a
  YAML list for easy python decoding and a function that builds an
  array for Bash elements.


.. _diskimage-builder_2.0.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/dibv2-omnibus-b30e0c7ecd76db8d.yaml @ 6887e796e10b57b55ee01965b48e6e698cede520

- A number of long-deprecated elements have been removed in v2, which
  are to the best of our knowledge unused.
  
  - ``partitioning-sfdisk``
  - ``deploy-ironic-element``
  - ``ironc-discovered-ramdisk``
  - ``serial-console-element``
  - ``map-services``

.. releasenotes/notes/dibv2-omnibus-b30e0c7ecd76db8d.yaml @ 6887e796e10b57b55ee01965b48e6e698cede520

- We have removed and deprecated the ``dib-utils`` package.  This
  was intended to be a more generic repository of tools that might
  be useful outside dib, but that did not eventuate and it has been
  folded back into dib for simplicity.


.. _diskimage-builder_2.0.0rc1:

2.0.0rc1
========

.. _diskimage-builder_2.0.0rc1_New Features:

New Features
------------

.. releasenotes/notes/doc-auto-element-dependency-cb7488c5bb7301a4.yaml @ fdd2c4b2361bb9f088d8723a6fafbdf5c4101c5d

- Create sphinx directive 'element_deps' that automatically generates dependencies in the element documentation.


.. _diskimage-builder_1.27.0:

1.27.0
======

.. _diskimage-builder_1.27.0_New Features:

New Features
------------

.. releasenotes/notes/move_tidy_logs_to_main-a8c03427fe1a445c.yaml @ 022d93ee822e71245af52c4cf8f8a8e82f599af3

- Cleaning logs was split, some was done in the img-functions.finalise_base, some was done in the base element. The version unifies tidy up logs in the lib/img-functions. Especially when building docker container images the base element cannot be used. This patch removes about some hundreds KB of useless logs in cases when the base element is not used.


.. _diskimage-builder_1.27.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/yum-cache-removal-148c33012515e56e.yaml @ 4585955a8b82889c61deb9ecb34b8713270406a7

- The ``DIB_YUMCHROOT_USE_CACHE`` variable has been removed and the Fedora and CentOS ``-minimal`` initial chroot will always be created by the package manager.  The default creation of a chroot tarball is stopped for these elements.  This unused option was unsafe; there is no guarantee that the base system will not change even between runs.  Getting the package manager to reuse the cache for the initial chroot install is future work.


.. _diskimage-builder_1.26.0:

1.26.0
======

.. _diskimage-builder_1.26.0_New Features:

New Features
------------

.. releasenotes/notes/grub-timeout-1cdd14a2b1467d89.yaml @ 61087d33e9ef67f05ef4a3b0dfc90ab521604292

- The ``bootloader`` element will explicitly set the timeout to ``5`` seconds when using ``grub`` (previously this was undefined, but platform defaults were usually 5 seconds).  Set this to ``0`` for faster boots.

.. releasenotes/notes/squashfs-output-91c1f0dc37474d3c.yaml @ 9d13084c4183b63587e1f5e4b03395a8df6538f6

- New squashfs image output format.


.. _diskimage-builder_1.24.0:

1.24.0
======

.. _diskimage-builder_1.24.0_New Features:

New Features
------------

.. releasenotes/notes/block-device-partitioning-237249e7ed2bad26.yaml @ ec7f56c1b2d8aa385751f02a3fa82e5a13d20b9d

- Create partitions with MBR layout optimized for performance and highly configurable.


.. _diskimage-builder_1.24.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/block-device-partitioning-237249e7ed2bad26.yaml @ ec7f56c1b2d8aa385751f02a3fa82e5a13d20b9d

- The new partitions are created based on configuration rather than on a list of provided commands for a special partitioning tool. Therefore elements using tools (like partitioning-sfdisk) are deprecated and will be removed.


.. _diskimage-builder_1.24.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/package-outside-debootstrap-ac93e9ce991819f1.yaml @ 45df304d488a0309fb981a4964238b81a370c358

- The `debian-minimal` and and `ubuntu-minimal` elements now install directly from the updates repo, avoiding the need to double-install packages during build.


.. _diskimage-builder_1.23.0:

1.23.0
======

.. _diskimage-builder_1.23.0_New Features:

New Features
------------

.. releasenotes/notes/openssh-server-0f6d065748a2fc18.yaml @ bbcc22751f689fb1002a85e641a854006280ad66

- New openssh-server element to ensure that the openssh server is installed and enabled during boot.


.. _diskimage-builder_1.22.0:

1.22.0
======

.. _diskimage-builder_1.22.0_New Features:

New Features
------------

.. releasenotes/notes/opensuse-minimal-45267f5be1112c22.yaml @ 90536dbab3e425d71a626f534307304389a2b7fd

- New zypper-minimal and opensuse-minimal elements to create basic openSUSE images. These two new elements are also making use of the existing zypper element which has been extended to include the functionality previously present in the opensuse element.


.. _diskimage-builder_1.22.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/remove-dib-utils-37f70dfad54900a0.yaml @ d65678678ec0416550d768f323ceace4d0861bca

- The `dib-utils` requirement has been removed as the `dib-run-parts` script is now shipped from within diskimage-builder.  The `dib-utils` project is now considered retired.


.. _diskimage-builder_1.20.0:

1.20.0
======

.. _diskimage-builder_1.20.0_New Features:

New Features
------------

.. releasenotes/notes/block-device-handling-279cddba8a859718.yaml @ 19efc60ce8ee7abecb847b01ef1e78f3160cdaa4

- Add new block device handling. Unify and generalize the creation and usage of block device.  This release includes setting up the general infrastructure and setting up loop device

.. releasenotes/notes/element-vars-c6bf2e6795002f01.yaml @ 37a53354ec51a1d20c3ac7bfa70744fa858dcb88

- Elements that need access to the other elements being used during the build should use the new ``IMAGE_ELEMENT_YAML`` environment variable and it's Bash equivalent ``get_image_element_array``.

.. releasenotes/notes/runtime-ssh-host-keys-7a2fc873cc90d33e.yaml @ 45467e4229b6222c63a1d274331c6fe81bca8442

- New element (runtime-ssh-host-keys) to manage SSH host keys at boot. Since SSH host key generation is not standard across operating systems, add support for both Debian and Ubuntu to handle it. While this is a new element, simple-init has been updated to depend on it.


.. _diskimage-builder_1.20.0_Known Issues:

Known Issues
------------

.. releasenotes/notes/block-device-handling-279cddba8a859718.yaml @ 19efc60ce8ee7abecb847b01ef1e78f3160cdaa4

- Because the implementation of the new block device layer is not complete, some features which are already implemented cannot be used because of limitations of the current environment.


.. _diskimage-builder_1.20.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/block-device-handling-279cddba8a859718.yaml @ 19efc60ce8ee7abecb847b01ef1e78f3160cdaa4

- The current way of handling block devices is deprecated. The existing block device phase will be called for a limited time.  If this phase delivers a result, this is used; if there is no result, the new way of block device handling is used. Please note that the old way of block device handling has some major limitations such as that it is only possible to use one block device.

.. releasenotes/notes/block-device-handling-279cddba8a859718.yaml @ 19efc60ce8ee7abecb847b01ef1e78f3160cdaa4

- The element 'partitioning-sfdisk' is deprecated.  The new implementation will create the partition tables based on a tool independent description.

.. releasenotes/notes/element-info-entry-point-448bf622be6061a0.yaml @ 91b431ce7864b0bf04ef88c71b185f3f8f5a246b

- The ``element-info`` script is now provided by a standard python entry-point, rather than an explicit wrapper script.  This may affect you if you were running this script directly out of ``bin`` in the source directory without installing.  See developer notes for details on using developer-installs with virtual environments for testing.

.. releasenotes/notes/element-override-ccda78c24ab4a4ff.yaml @ 274be6de551883fc14e3af30f84ba5bdf829814e

- Element override behavior is now defined, with elements found in earlier entries of ``ELEMENTS_PATH`` overriding later ones (e.g. the same semantics as ``$PATH``).  Previously the behavior was undefined.

