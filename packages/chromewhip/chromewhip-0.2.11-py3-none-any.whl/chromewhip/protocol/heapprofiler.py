# noinspection PyPep8
# noinspection PyArgumentList

"""
AUTO-GENERATED BY `scripts/generate_protocol.py` using `data/browser_protocol.json`
and `data/js_protocol.json` as inputs! Please do not modify this file.
"""

import logging
from typing import Any, Optional, Union

from chromewhip.helpers import PayloadMixin, BaseEvent, ChromeTypeBase

log = logging.getLogger(__name__)
from chromewhip.protocol import runtime as Runtime

# HeapSnapshotObjectId: Heap snapshot object id.
HeapSnapshotObjectId = str

# SamplingHeapProfileNode: Sampling Heap Profile node. Holds callsite information, allocation statistics and child nodes.
class SamplingHeapProfileNode(ChromeTypeBase):
    def __init__(self,
                 callFrame: Union['Runtime.CallFrame'],
                 selfSize: Union['float'],
                 children: Union['[SamplingHeapProfileNode]'],
                 ):

        self.callFrame = callFrame
        self.selfSize = selfSize
        self.children = children


# SamplingHeapProfile: Profile.
class SamplingHeapProfile(ChromeTypeBase):
    def __init__(self,
                 head: Union['SamplingHeapProfileNode'],
                 ):

        self.head = head


class HeapProfiler(PayloadMixin):
    """ 
    """
    @classmethod
    def addInspectedHeapObject(cls,
                               heapObjectId: Union['HeapSnapshotObjectId'],
                               ):
        """Enables console to refer to the node with given id via $x (see Command Line API for more details
$x functions).
        :param heapObjectId: Heap snapshot object id to be accessible by means of $x command line API.
        :type heapObjectId: HeapSnapshotObjectId
        """
        return (
            cls.build_send_payload("addInspectedHeapObject", {
                "heapObjectId": heapObjectId,
            }),
            None
        )

    @classmethod
    def collectGarbage(cls):
        """
        """
        return (
            cls.build_send_payload("collectGarbage", {
            }),
            None
        )

    @classmethod
    def disable(cls):
        """
        """
        return (
            cls.build_send_payload("disable", {
            }),
            None
        )

    @classmethod
    def enable(cls):
        """
        """
        return (
            cls.build_send_payload("enable", {
            }),
            None
        )

    @classmethod
    def getHeapObjectId(cls,
                        objectId: Union['Runtime.RemoteObjectId'],
                        ):
        """
        :param objectId: Identifier of the object to get heap object id for.
        :type objectId: Runtime.RemoteObjectId
        """
        return (
            cls.build_send_payload("getHeapObjectId", {
                "objectId": objectId,
            }),
            cls.convert_payload({
                "heapSnapshotObjectId": {
                    "class": HeapSnapshotObjectId,
                    "optional": False
                },
            })
        )

    @classmethod
    def getObjectByHeapObjectId(cls,
                                objectId: Union['HeapSnapshotObjectId'],
                                objectGroup: Optional['str'] = None,
                                ):
        """
        :param objectId: 
        :type objectId: HeapSnapshotObjectId
        :param objectGroup: Symbolic group name that can be used to release multiple objects.
        :type objectGroup: str
        """
        return (
            cls.build_send_payload("getObjectByHeapObjectId", {
                "objectId": objectId,
                "objectGroup": objectGroup,
            }),
            cls.convert_payload({
                "result": {
                    "class": Runtime.RemoteObject,
                    "optional": False
                },
            })
        )

    @classmethod
    def getSamplingProfile(cls):
        """
        """
        return (
            cls.build_send_payload("getSamplingProfile", {
            }),
            cls.convert_payload({
                "profile": {
                    "class": SamplingHeapProfile,
                    "optional": False
                },
            })
        )

    @classmethod
    def startSampling(cls,
                      samplingInterval: Optional['float'] = None,
                      ):
        """
        :param samplingInterval: Average sample interval in bytes. Poisson distribution is used for the intervals. The
default value is 32768 bytes.
        :type samplingInterval: float
        """
        return (
            cls.build_send_payload("startSampling", {
                "samplingInterval": samplingInterval,
            }),
            None
        )

    @classmethod
    def startTrackingHeapObjects(cls,
                                 trackAllocations: Optional['bool'] = None,
                                 ):
        """
        :param trackAllocations: 
        :type trackAllocations: bool
        """
        return (
            cls.build_send_payload("startTrackingHeapObjects", {
                "trackAllocations": trackAllocations,
            }),
            None
        )

    @classmethod
    def stopSampling(cls):
        """
        """
        return (
            cls.build_send_payload("stopSampling", {
            }),
            cls.convert_payload({
                "profile": {
                    "class": SamplingHeapProfile,
                    "optional": False
                },
            })
        )

    @classmethod
    def stopTrackingHeapObjects(cls,
                                reportProgress: Optional['bool'] = None,
                                ):
        """
        :param reportProgress: If true 'reportHeapSnapshotProgress' events will be generated while snapshot is being taken
when the tracking is stopped.
        :type reportProgress: bool
        """
        return (
            cls.build_send_payload("stopTrackingHeapObjects", {
                "reportProgress": reportProgress,
            }),
            None
        )

    @classmethod
    def takeHeapSnapshot(cls,
                         reportProgress: Optional['bool'] = None,
                         ):
        """
        :param reportProgress: If true 'reportHeapSnapshotProgress' events will be generated while snapshot is being taken.
        :type reportProgress: bool
        """
        return (
            cls.build_send_payload("takeHeapSnapshot", {
                "reportProgress": reportProgress,
            }),
            None
        )



class AddHeapSnapshotChunkEvent(BaseEvent):

    js_name = 'Heapprofiler.addHeapSnapshotChunk'
    hashable = []
    is_hashable = False

    def __init__(self,
                 chunk: Union['str', dict],
                 ):
        if isinstance(chunk, dict):
            chunk = str(**chunk)
        self.chunk = chunk

    @classmethod
    def build_hash(cls):
        raise ValueError('Unable to build hash for non-hashable type')


class HeapStatsUpdateEvent(BaseEvent):

    js_name = 'Heapprofiler.heapStatsUpdate'
    hashable = []
    is_hashable = False

    def __init__(self,
                 statsUpdate: Union['[]', dict],
                 ):
        if isinstance(statsUpdate, dict):
            statsUpdate = [](**statsUpdate)
        self.statsUpdate = statsUpdate

    @classmethod
    def build_hash(cls):
        raise ValueError('Unable to build hash for non-hashable type')


class LastSeenObjectIdEvent(BaseEvent):

    js_name = 'Heapprofiler.lastSeenObjectId'
    hashable = ['lastSeenObjectId']
    is_hashable = True

    def __init__(self,
                 lastSeenObjectId: Union['int', dict],
                 timestamp: Union['float', dict],
                 ):
        if isinstance(lastSeenObjectId, dict):
            lastSeenObjectId = int(**lastSeenObjectId)
        self.lastSeenObjectId = lastSeenObjectId
        if isinstance(timestamp, dict):
            timestamp = float(**timestamp)
        self.timestamp = timestamp

    @classmethod
    def build_hash(cls, lastSeenObjectId):
        kwargs = locals()
        kwargs.pop('cls')
        serialized_id_params = ','.join(['='.join([p, str(v)]) for p, v in kwargs.items()])
        h = '{}:{}'.format(cls.js_name, serialized_id_params)
        log.debug('generated hash = %s' % h)
        return h


class ReportHeapSnapshotProgressEvent(BaseEvent):

    js_name = 'Heapprofiler.reportHeapSnapshotProgress'
    hashable = []
    is_hashable = False

    def __init__(self,
                 done: Union['int', dict],
                 total: Union['int', dict],
                 finished: Union['bool', dict, None] = None,
                 ):
        if isinstance(done, dict):
            done = int(**done)
        self.done = done
        if isinstance(total, dict):
            total = int(**total)
        self.total = total
        if isinstance(finished, dict):
            finished = bool(**finished)
        self.finished = finished

    @classmethod
    def build_hash(cls):
        raise ValueError('Unable to build hash for non-hashable type')


class ResetProfilesEvent(BaseEvent):

    js_name = 'Heapprofiler.resetProfiles'
    hashable = []
    is_hashable = False

    def __init__(self):
        pass

    @classmethod
    def build_hash(cls):
        raise ValueError('Unable to build hash for non-hashable type')
