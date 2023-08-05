Voxpopuli
=========

|PyPI| |PyPI| |license|

**A wrapper around Espeak and Mbrola.**

This is a lightweight Python wrapper for Espeak and Mbrola, two
co-dependent TTS tools. It enables you to render sound by simply feeding
it text and voice parameters. Phonems (the data transmitted by Espeak to
mbrola) can also be manipulated using a mimalistic API.

Install
-------

Install with pip as:

.. code:: sh

    pip install voxpopuli

You have to have espeak and mbrola installed beforehand:

.. code:: sh

    sudo apt install mbrola espeak

You'll also need some mbrola voices installed, which you can either get
on their project page, and then uppack in
``/usr/share/mbrola/<lang><voiceid>/`` or more simply by installing them
from the ubuntu repo's. All the voices' packages are of the form
``mbrola-<lang><voiceid>``. You can more simply install all the voices
available by running:

.. code:: sh

    sudo apt install mbrola-*

Usage
-----

Picking a voice and making it say things
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most simple usage of this lib is just bare TTS, using a voice and a
text. The rendered audio is returned in a .wav bytes object:

.. code:: python

    from voxpopuli import Voice
    voice = Voice(lang="fr")
    wav = voice.to_audio("salut c'est cool")

Evaluating ``type(wav)`` whould return ``bytes``. You can then save the
wav using the ``wb`` file option

.. code:: python

    with open("salut.wav", "wb") as wavfile:
        wavfile.write(wav)

If you wish to hear how it sounds right away, you can always do :

.. code:: python

    voice.say("Salut c'est cool")

Ou can also, say, use scipy to get the pcm audio as a ``ndarray``:

.. code:: python

    import scipy.io.wavfile import read, write
    from io import BytesIO

    rate, wave_array = read(wav)
    reversed = wave_array[::-1] # reversing the sound file
    write("tulas.wav", rate, reversed)

Getting different voices
~~~~~~~~~~~~~~~~~~~~~~~~

You can set some parameters you can set on the voice, such as language
or pitch

.. code:: python

    from voxpopuli import Voice
    # really slow fice with high pitch
    voice = Voice(lang="us", pitch="99", speed="50", voice_id=2)
    voice.say("I'm high on helium")

The exhaustive list of parameters is:

-  lang, a language code among those available (us, fr, en, es, ...) You
   can list them using the ``listvoices`` method from a ``Voice``
   instance.
-  voice\_id, an integer, used to select the voice id for a language. If
   not specified, the first voice id found for a given language is used.
-  pitch, an integer between 0 and 99 (included)
-  speed, an integer, in the words per minute. Default and regular speed
   is 160 wpm.
-  volume, float ratio applied to the output sample. Some languages have
   presets that our best specialists tested. Otherwise, defaults to 1.

Handling the phonemic form
~~~~~~~~~~~~~~~~~~~~~~~~~~

To render a string of text to audio, the Voice object actually chains
espeak's output to mbrola, who then renders it to audio. Espeak only
renders the text to a list of phonems (such as the one in the IPA), who
then are to be processed by mbrola. For those who like pictures, here is
a diagram of what happens when you run ``voice.to_audio("Hello world")``

.. figure:: doc/phonems.png?raw=true
   :alt: Phonems

   Phonems

Phonems are represented sequentially by a code, a duration in
milliseconds, and a list of pitch modifiers. The pitch modifiers are a
list of couples, each couple representing the percentage of the sample
at which to apply the pitch modification and the pitch.

Funny thing is, with voxpopuli, you can ``intercept`` that phonemlist as
a simple object, modify it, and then pass it back to the voice to render
it to audio. For instance, let's make a simple alteration that'll double
the duration for each vowels in an english text.

.. code:: python

    from voxpopuli import Voice, EnglishPhonems

    voice = Voice(lang="en")
    # here's how you get the phonems list
    phonem_list = voice.to_phonems("Now go away or I will taunt you a second time.") 
    for phonem in phonem_list: #phonem list object inherits from the list object
        if phonem.name in EnglishPhonems.VOWELS:
            phonem.duration *= 3
            
    # rendering and saving the sound, then saying it out loud:
    voice.to_audio(phonem_list, "modified.wav")
    voice.say(phonem_list)

Notes:

-  For French, Spanish, American English, British English and german,
   the phonem codes used by espeak and mbrola are available as class
   attributes like in the ``EnglishPhonems`` class used before.
-  More info on the phonems can be found here: `SAMPA
   page <http://www.phon.ucl.ac.uk/home/sampa/>`__

What's left to do
-----------------

-  A real sphinx documentation
-  Moar unit tests
-  Maybe some examples

.. |PyPI| image:: https://img.shields.io/pypi/v/voxpopuli.svg
   :target: https://pypi.python.org/pypi/voxpopuli
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/voxpopuli.svg
   :target: http://py3readiness.org/
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: LICENSE
