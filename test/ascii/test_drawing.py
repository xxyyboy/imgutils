from unittest import mock

import pytest

from imgutils.ascii import ascii_drawing
from test.testings import get_testfile


@pytest.fixture(scope='module', autouse=True)
def fake_terminal_size():
    with mock.patch.dict('os.environ', {'LINES': '40', 'COLUMNS': '80'}):
        yield


@pytest.fixture()
def jerry():
    return get_testfile('jerry_with_space_squeeze.png')


@pytest.fixture()
def star():
    return get_testfile('star.png')


@pytest.mark.unittest
class TestAsciiDrawing:
    def test_ascii_drawing(self, jerry, star, text_aligner):
        text_aligner.assert_equal(
            ascii_drawing(jerry),
            """
          .=-.
          ==-:.
        .-++=:=.   .-==-
         =++*++=: .===-:-
       .-+=======-===:::-.
      :++======-====::::-:
      ++===++==---=:::::-:
     :++=-=--=---=-:::::-:
     :=.-== :=---=-:::::=.
     .-.==. =----===::::=
     .=:==..=-----==:::=:
   .-=+==+:-=-----=::::=
   .+=-=-::=====-=-:::=.
   .+=.-:.-+======::-=.
    :+:   :+===-=---:
     :-..  :===++--:.  ..
       ...:-++++===++===:
         -=====-------==--...
        .=====------===----==-
        ====::=--====-=+-=--==:
       .+==::.-===-   .=-=--==.
       :+-===::-=-==-: .==  ::
       .+----=====--===::+:
        =====--==--=--=+++:
         ::--=-==..-=--=*-
            --===..:=---==
            :-:::...-----+:
             -=:....=----==
            .==+=--==-----=:
            ==--===-:==-----
           .=---=-    :==--=.
            ==--=       -=--=-::
           .===-=.       .==-====
           :=---=-        .==--==
            -==++.         .====:
            """
        )
        text_aligner.assert_equal(
            ascii_drawing(star),
            """
                    .:.
                    .:.
                    :::
                   .:::.
                   .:::.
             .:::::::::::::::.
             .:::::::::::::::.
              .:::::::::::::.
                :::::::::::
                 .:::::::.
                 .:::::::.
                 :::::::::
                .:::::::::.
                .:::   :::.
                ::.     .::
                 .       .
            """
        )