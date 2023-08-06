
Release 1.0a6 on 3. Oct 2018
----------------------------

- Added packet counter checks to detect lost packets and to detect
  potential mis-alignment of signals from various streams.
- In trigger single shot mode when signal is acquired, generator
  exists and consequently MonoDAQ_U stops streaming. So in the
  following example number of samples may be used as timeout until
  the first triggering:

    signal.trigger( mdu.fetch(2000000), precond='DI1 < 0.5', cond='DI1 > 0.5',
                    P=200, N=200, single_shot=True)

- MonoDAQ_U: added support for 7 channels


Release 1.0a5 on 30. Sep 2018
------------------------------

- First published release supporting Isotel Precision & MonoDAQ-U-X products