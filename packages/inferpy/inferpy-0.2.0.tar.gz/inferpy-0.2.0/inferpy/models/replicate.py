# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


"""Module with the replication functionality.
"""

from functools import reduce

class replicate():
    """Class implementing the Plateau notation

        The plateau notation is used to replicate the random variables contained
        within this construct. Every replicated variable is conditionally idependent
        given the previous random variables (if any) defined outside the with statement.
        The ``with inf.replicate(size = N)`` sintaxis is used to replicate N times the
        contained definitions. For example:

        .. literalinclude:: ../../examples/replicate_nested.py


        The number of times that indicated with input argument ``size``.
        Note that nested replicate constructs can be defined as well. At any moment,
        the product of all the nested replicate constructs can be obtained by
        invoking the static method ``get_total_size()``.

        .. note::

            Defining a variable inside the construct replicate with size equal to 1, that is,
            ``inf.replicate(size=1)`` is equivalent to defining outside any replicate
            construct.


        """


    __active_rep = []
    __all_rep = []

    def __init__(self,size):
        """Initializes the replicate construct

        Args:
            size (int): number of times that the variables contained are replicated.

        """
        self.size = size

        self.varlist=[]

    @staticmethod
    def __get_all_sizes():
        return [1]+[r.size for r in replicate.__active_rep]


    def __enter__(self):
        replicate.__active_rep.append(self)
        replicate.__all_rep.append(self)


        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        replicate.__active_rep.pop()



    @staticmethod
    def get_total_size():
        """Static method that returns the product of the sizes of all the nested replicate constructs

        Returns:
            Integer with the product of sizes

        """
        if len(replicate.__get_all_sizes()) == 1:
            return 1
        return reduce(lambda x, y: x * y, replicate.__get_all_sizes())

    @staticmethod
    def print_total_size():
        """Static that prints the total size
        """
        print("total size: " + str(replicate.get_total_size()))

    @staticmethod
    def in_replicate():
        """Check if a replicate construct has been initialized

        Returns:
             True if the method is inside a construct replicate (of size different to 1).
             Otherwise False is return
        """
        return len(replicate.__active_rep)>0



    # static methods
    @staticmethod
    def get_active_replicate():

        """ Return the active replicate defined with the construct 'with' """

        if replicate.in_replicate():
            return replicate.__active_rep
        return []

    @staticmethod
    def get_all_replicate():
        return replicate.__all_rep

