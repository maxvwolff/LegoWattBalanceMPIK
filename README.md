# Development and measurements with a LEGO wattbalance

By now, the kilogram is officially defined by the so-called IPK (International Prototype Kilogram), safely stored in Paris. It is basically a cylindrical piece of metal made up of a platin alloy.
Several problems come with this kind of definition of a unit, one of them being that it is defined by an aribtrarily chosen amount of matter – instead of fundamental constants of nature.

This is where the principle of the watt balance comes into play. Since it can measure an arbitrarily chosen amount of mass in terms of electrical units, it is able to link the kilogram with e.g. Planck's Constant.
One of the by far most sophisticated ones is in the possession of NIST, with an uncertainty in measurement of Planck's constant of just 34 parts per billion.

The aim of this project, however, is to investigate, what measurement uncertainties can be achieved with rather simple and not as cost-sensitive methods.

# The main working principle

For the determination of a test mass, the weight of the test mass is simply cancelled out by a Laplace force, created by an electromagnet.
This is done by placing the test mass on one side of a balance beam and the coil producing a downward force on the other side, such that the balance beam is in an exactly horizontal position if the two forces cancel out.

By measuring the electrical current through the coil, the precise earth's acceleration and the magnetic flux integral regarding the coil in the magnetic field created by permanent magnets, it would theoretically be possible to
determine the mass of the test object. But since it is nearly impossibe to accurately measure the magnetic flux integral, we incorporate a second mode of operation into our measurement, which enables us to accurately measure this
missing component. This mode is called the velocity mode. Now, the coil is moved through the magnetic field and as a consequence, a voltage is induced into the coil.
The precise measurement of this induced voltage and the speed at which the coil is moved through the magnetic field, we can obtain the magnetic flux integral – and in conclusion, determine the mass of our test object!

# Technical implementation
Besides the technical aspects of the project, in the end, a variety of processes had to be controlled numerically by the means of control software incorporating PID controllers, filters and so on.
Because of the broad accessibility of scientific modules and it's simplicity, Python 3 was the programming language of choice.

The self-developed watt balance: 
![Watt balance](https://github.com/maxvwolff/LegoWattBalanceMPIK/blob/master/Assetes/img/IMG_5068.JPG)
