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

# ScriptId: Unique script identifier.
ScriptId = str

# RemoteObjectId: Unique object identifier.
RemoteObjectId = str

# UnserializableValue: Primitive value which cannot be JSON-stringified. Includes values `-0`, `NaN`, `Infinity`,`-Infinity`, and bigint literals.
UnserializableValue = str

# RemoteObject: Mirror object referencing original JavaScript object.
class RemoteObject(ChromeTypeBase):
    def __init__(self,
                 type: Union['str'],
                 subtype: Optional['str'] = None,
                 className: Optional['str'] = None,
                 value: Optional['Any'] = None,
                 unserializableValue: Optional['UnserializableValue'] = None,
                 description: Optional['str'] = None,
                 objectId: Optional['RemoteObjectId'] = None,
                 preview: Optional['ObjectPreview'] = None,
                 customPreview: Optional['CustomPreview'] = None,
                 ):

        self.type = type
        self.subtype = subtype
        self.className = className
        self.value = value
        self.unserializableValue = unserializableValue
        self.description = description
        self.objectId = objectId
        self.preview = preview
        self.customPreview = customPreview


# CustomPreview: 
class CustomPreview(ChromeTypeBase):
    def __init__(self,
                 header: Union['str'],
                 hasBody: Union['bool'],
                 formatterObjectId: Union['RemoteObjectId'],
                 bindRemoteObjectFunctionId: Union['RemoteObjectId'],
                 configObjectId: Optional['RemoteObjectId'] = None,
                 ):

        self.header = header
        self.hasBody = hasBody
        self.formatterObjectId = formatterObjectId
        self.bindRemoteObjectFunctionId = bindRemoteObjectFunctionId
        self.configObjectId = configObjectId


# ObjectPreview: Object containing abbreviated remote object value.
class ObjectPreview(ChromeTypeBase):
    def __init__(self,
                 type: Union['str'],
                 overflow: Union['bool'],
                 properties: Union['[PropertyPreview]'],
                 subtype: Optional['str'] = None,
                 description: Optional['str'] = None,
                 entries: Optional['[EntryPreview]'] = None,
                 ):

        self.type = type
        self.subtype = subtype
        self.description = description
        self.overflow = overflow
        self.properties = properties
        self.entries = entries


# PropertyPreview: 
class PropertyPreview(ChromeTypeBase):
    def __init__(self,
                 name: Union['str'],
                 type: Union['str'],
                 value: Optional['str'] = None,
                 valuePreview: Optional['ObjectPreview'] = None,
                 subtype: Optional['str'] = None,
                 ):

        self.name = name
        self.type = type
        self.value = value
        self.valuePreview = valuePreview
        self.subtype = subtype


# EntryPreview: 
class EntryPreview(ChromeTypeBase):
    def __init__(self,
                 value: Union['ObjectPreview'],
                 key: Optional['ObjectPreview'] = None,
                 ):

        self.key = key
        self.value = value


# PropertyDescriptor: Object property descriptor.
class PropertyDescriptor(ChromeTypeBase):
    def __init__(self,
                 name: Union['str'],
                 configurable: Union['bool'],
                 enumerable: Union['bool'],
                 value: Optional['RemoteObject'] = None,
                 writable: Optional['bool'] = None,
                 get: Optional['RemoteObject'] = None,
                 set: Optional['RemoteObject'] = None,
                 wasThrown: Optional['bool'] = None,
                 isOwn: Optional['bool'] = None,
                 symbol: Optional['RemoteObject'] = None,
                 ):

        self.name = name
        self.value = value
        self.writable = writable
        self.get = get
        self.set = set
        self.configurable = configurable
        self.enumerable = enumerable
        self.wasThrown = wasThrown
        self.isOwn = isOwn
        self.symbol = symbol


# InternalPropertyDescriptor: Object internal property descriptor. This property isn't normally visible in JavaScript code.
class InternalPropertyDescriptor(ChromeTypeBase):
    def __init__(self,
                 name: Union['str'],
                 value: Optional['RemoteObject'] = None,
                 ):

        self.name = name
        self.value = value


# CallArgument: Represents function call argument. Either remote object id `objectId`, primitive `value`,unserializable primitive value or neither of (for undefined) them should be specified.
class CallArgument(ChromeTypeBase):
    def __init__(self,
                 value: Optional['Any'] = None,
                 unserializableValue: Optional['UnserializableValue'] = None,
                 objectId: Optional['RemoteObjectId'] = None,
                 ):

        self.value = value
        self.unserializableValue = unserializableValue
        self.objectId = objectId


# ExecutionContextId: Id of an execution context.
ExecutionContextId = int

# ExecutionContextDescription: Description of an isolated world.
class ExecutionContextDescription(ChromeTypeBase):
    def __init__(self,
                 id: Union['ExecutionContextId'],
                 origin: Union['str'],
                 name: Union['str'],
                 auxData: Optional['dict'] = None,
                 ):

        self.id = id
        self.origin = origin
        self.name = name
        self.auxData = auxData


# ExceptionDetails: Detailed information about exception (or error) that was thrown during script compilation orexecution.
class ExceptionDetails(ChromeTypeBase):
    def __init__(self,
                 exceptionId: Union['int'],
                 text: Union['str'],
                 lineNumber: Union['int'],
                 columnNumber: Union['int'],
                 scriptId: Optional['ScriptId'] = None,
                 url: Optional['str'] = None,
                 stackTrace: Optional['StackTrace'] = None,
                 exception: Optional['RemoteObject'] = None,
                 executionContextId: Optional['ExecutionContextId'] = None,
                 ):

        self.exceptionId = exceptionId
        self.text = text
        self.lineNumber = lineNumber
        self.columnNumber = columnNumber
        self.scriptId = scriptId
        self.url = url
        self.stackTrace = stackTrace
        self.exception = exception
        self.executionContextId = executionContextId


# Timestamp: Number of milliseconds since epoch.
Timestamp = float

# TimeDelta: Number of milliseconds.
TimeDelta = float

# CallFrame: Stack entry for runtime errors and assertions.
class CallFrame(ChromeTypeBase):
    def __init__(self,
                 functionName: Union['str'],
                 scriptId: Union['ScriptId'],
                 url: Union['str'],
                 lineNumber: Union['int'],
                 columnNumber: Union['int'],
                 ):

        self.functionName = functionName
        self.scriptId = scriptId
        self.url = url
        self.lineNumber = lineNumber
        self.columnNumber = columnNumber


# StackTrace: Call frames for assertions or error messages.
class StackTrace(ChromeTypeBase):
    def __init__(self,
                 callFrames: Union['[CallFrame]'],
                 description: Optional['str'] = None,
                 parent: Optional['StackTrace'] = None,
                 parentId: Optional['StackTraceId'] = None,
                 ):

        self.description = description
        self.callFrames = callFrames
        self.parent = parent
        self.parentId = parentId


# UniqueDebuggerId: Unique identifier of current debugger.
UniqueDebuggerId = str

# StackTraceId: If `debuggerId` is set stack trace comes from another debugger and can be resolved there. Thisallows to track cross-debugger calls. See `Runtime.StackTrace` and `Debugger.paused` for usages.
class StackTraceId(ChromeTypeBase):
    def __init__(self,
                 id: Union['str'],
                 debuggerId: Optional['UniqueDebuggerId'] = None,
                 ):

        self.id = id
        self.debuggerId = debuggerId


class Runtime(PayloadMixin):
    """ Runtime domain exposes JavaScript runtime by means of remote evaluation and mirror objects.
Evaluation results are returned as mirror object that expose object type, string representation
and unique identifier that can be used for further object reference. Original objects are
maintained in memory unless they are either explicitly released or are released along with the
other objects in their object group.
    """
    @classmethod
    def awaitPromise(cls,
                     promiseObjectId: Union['RemoteObjectId'],
                     returnByValue: Optional['bool'] = None,
                     generatePreview: Optional['bool'] = None,
                     ):
        """Add handler to promise with given promise object id.
        :param promiseObjectId: Identifier of the promise.
        :type promiseObjectId: RemoteObjectId
        :param returnByValue: Whether the result is expected to be a JSON object that should be sent by value.
        :type returnByValue: bool
        :param generatePreview: Whether preview should be generated for the result.
        :type generatePreview: bool
        """
        return (
            cls.build_send_payload("awaitPromise", {
                "promiseObjectId": promiseObjectId,
                "returnByValue": returnByValue,
                "generatePreview": generatePreview,
            }),
            cls.convert_payload({
                "result": {
                    "class": RemoteObject,
                    "optional": False
                },
                "exceptionDetails": {
                    "class": ExceptionDetails,
                    "optional": True
                },
            })
        )

    @classmethod
    def callFunctionOn(cls,
                       functionDeclaration: Union['str'],
                       objectId: Optional['RemoteObjectId'] = None,
                       arguments: Optional['[CallArgument]'] = None,
                       silent: Optional['bool'] = None,
                       returnByValue: Optional['bool'] = None,
                       generatePreview: Optional['bool'] = None,
                       userGesture: Optional['bool'] = None,
                       awaitPromise: Optional['bool'] = None,
                       executionContextId: Optional['ExecutionContextId'] = None,
                       objectGroup: Optional['str'] = None,
                       ):
        """Calls function with given declaration on the given object. Object group of the result is
inherited from the target object.
        :param functionDeclaration: Declaration of the function to call.
        :type functionDeclaration: str
        :param objectId: Identifier of the object to call function on. Either objectId or executionContextId should
be specified.
        :type objectId: RemoteObjectId
        :param arguments: Call arguments. All call arguments must belong to the same JavaScript world as the target
object.
        :type arguments: [CallArgument]
        :param silent: In silent mode exceptions thrown during evaluation are not reported and do not pause
execution. Overrides `setPauseOnException` state.
        :type silent: bool
        :param returnByValue: Whether the result is expected to be a JSON object which should be sent by value.
        :type returnByValue: bool
        :param generatePreview: Whether preview should be generated for the result.
        :type generatePreview: bool
        :param userGesture: Whether execution should be treated as initiated by user in the UI.
        :type userGesture: bool
        :param awaitPromise: Whether execution should `await` for resulting value and return once awaited promise is
resolved.
        :type awaitPromise: bool
        :param executionContextId: Specifies execution context which global object will be used to call function on. Either
executionContextId or objectId should be specified.
        :type executionContextId: ExecutionContextId
        :param objectGroup: Symbolic group name that can be used to release multiple objects. If objectGroup is not
specified and objectId is, objectGroup will be inherited from object.
        :type objectGroup: str
        """
        return (
            cls.build_send_payload("callFunctionOn", {
                "functionDeclaration": functionDeclaration,
                "objectId": objectId,
                "arguments": arguments,
                "silent": silent,
                "returnByValue": returnByValue,
                "generatePreview": generatePreview,
                "userGesture": userGesture,
                "awaitPromise": awaitPromise,
                "executionContextId": executionContextId,
                "objectGroup": objectGroup,
            }),
            cls.convert_payload({
                "result": {
                    "class": RemoteObject,
                    "optional": False
                },
                "exceptionDetails": {
                    "class": ExceptionDetails,
                    "optional": True
                },
            })
        )

    @classmethod
    def compileScript(cls,
                      expression: Union['str'],
                      sourceURL: Union['str'],
                      persistScript: Union['bool'],
                      executionContextId: Optional['ExecutionContextId'] = None,
                      ):
        """Compiles expression.
        :param expression: Expression to compile.
        :type expression: str
        :param sourceURL: Source url to be set for the script.
        :type sourceURL: str
        :param persistScript: Specifies whether the compiled script should be persisted.
        :type persistScript: bool
        :param executionContextId: Specifies in which execution context to perform script run. If the parameter is omitted the
evaluation will be performed in the context of the inspected page.
        :type executionContextId: ExecutionContextId
        """
        return (
            cls.build_send_payload("compileScript", {
                "expression": expression,
                "sourceURL": sourceURL,
                "persistScript": persistScript,
                "executionContextId": executionContextId,
            }),
            cls.convert_payload({
                "scriptId": {
                    "class": ScriptId,
                    "optional": True
                },
                "exceptionDetails": {
                    "class": ExceptionDetails,
                    "optional": True
                },
            })
        )

    @classmethod
    def disable(cls):
        """Disables reporting of execution contexts creation.
        """
        return (
            cls.build_send_payload("disable", {
            }),
            None
        )

    @classmethod
    def discardConsoleEntries(cls):
        """Discards collected exceptions and console API calls.
        """
        return (
            cls.build_send_payload("discardConsoleEntries", {
            }),
            None
        )

    @classmethod
    def enable(cls):
        """Enables reporting of execution contexts creation by means of `executionContextCreated` event.
When the reporting gets enabled the event will be sent immediately for each existing execution
context.
        """
        return (
            cls.build_send_payload("enable", {
            }),
            None
        )

    @classmethod
    def evaluate(cls,
                 expression: Union['str'],
                 objectGroup: Optional['str'] = None,
                 includeCommandLineAPI: Optional['bool'] = None,
                 silent: Optional['bool'] = None,
                 contextId: Optional['ExecutionContextId'] = None,
                 returnByValue: Optional['bool'] = None,
                 generatePreview: Optional['bool'] = None,
                 userGesture: Optional['bool'] = None,
                 awaitPromise: Optional['bool'] = None,
                 throwOnSideEffect: Optional['bool'] = None,
                 timeout: Optional['TimeDelta'] = None,
                 ):
        """Evaluates expression on global object.
        :param expression: Expression to evaluate.
        :type expression: str
        :param objectGroup: Symbolic group name that can be used to release multiple objects.
        :type objectGroup: str
        :param includeCommandLineAPI: Determines whether Command Line API should be available during the evaluation.
        :type includeCommandLineAPI: bool
        :param silent: In silent mode exceptions thrown during evaluation are not reported and do not pause
execution. Overrides `setPauseOnException` state.
        :type silent: bool
        :param contextId: Specifies in which execution context to perform evaluation. If the parameter is omitted the
evaluation will be performed in the context of the inspected page.
        :type contextId: ExecutionContextId
        :param returnByValue: Whether the result is expected to be a JSON object that should be sent by value.
        :type returnByValue: bool
        :param generatePreview: Whether preview should be generated for the result.
        :type generatePreview: bool
        :param userGesture: Whether execution should be treated as initiated by user in the UI.
        :type userGesture: bool
        :param awaitPromise: Whether execution should `await` for resulting value and return once awaited promise is
resolved.
        :type awaitPromise: bool
        :param throwOnSideEffect: Whether to throw an exception if side effect cannot be ruled out during evaluation.
        :type throwOnSideEffect: bool
        :param timeout: Terminate execution after timing out (number of milliseconds).
        :type timeout: TimeDelta
        """
        return (
            cls.build_send_payload("evaluate", {
                "expression": expression,
                "objectGroup": objectGroup,
                "includeCommandLineAPI": includeCommandLineAPI,
                "silent": silent,
                "contextId": contextId,
                "returnByValue": returnByValue,
                "generatePreview": generatePreview,
                "userGesture": userGesture,
                "awaitPromise": awaitPromise,
                "throwOnSideEffect": throwOnSideEffect,
                "timeout": timeout,
            }),
            cls.convert_payload({
                "result": {
                    "class": RemoteObject,
                    "optional": False
                },
                "exceptionDetails": {
                    "class": ExceptionDetails,
                    "optional": True
                },
            })
        )

    @classmethod
    def getIsolateId(cls):
        """Returns the isolate id.
        """
        return (
            cls.build_send_payload("getIsolateId", {
            }),
            cls.convert_payload({
                "id": {
                    "class": str,
                    "optional": False
                },
            })
        )

    @classmethod
    def getHeapUsage(cls):
        """Returns the JavaScript heap usage.
It is the total usage of the corresponding isolate not scoped to a particular Runtime.
        """
        return (
            cls.build_send_payload("getHeapUsage", {
            }),
            cls.convert_payload({
                "usedSize": {
                    "class": float,
                    "optional": False
                },
                "totalSize": {
                    "class": float,
                    "optional": False
                },
            })
        )

    @classmethod
    def getProperties(cls,
                      objectId: Union['RemoteObjectId'],
                      ownProperties: Optional['bool'] = None,
                      accessorPropertiesOnly: Optional['bool'] = None,
                      generatePreview: Optional['bool'] = None,
                      ):
        """Returns properties of a given object. Object group of the result is inherited from the target
object.
        :param objectId: Identifier of the object to return properties for.
        :type objectId: RemoteObjectId
        :param ownProperties: If true, returns properties belonging only to the element itself, not to its prototype
chain.
        :type ownProperties: bool
        :param accessorPropertiesOnly: If true, returns accessor properties (with getter/setter) only; internal properties are not
returned either.
        :type accessorPropertiesOnly: bool
        :param generatePreview: Whether preview should be generated for the results.
        :type generatePreview: bool
        """
        return (
            cls.build_send_payload("getProperties", {
                "objectId": objectId,
                "ownProperties": ownProperties,
                "accessorPropertiesOnly": accessorPropertiesOnly,
                "generatePreview": generatePreview,
            }),
            cls.convert_payload({
                "result": {
                    "class": [PropertyDescriptor],
                    "optional": False
                },
                "internalProperties": {
                    "class": [InternalPropertyDescriptor],
                    "optional": True
                },
                "exceptionDetails": {
                    "class": ExceptionDetails,
                    "optional": True
                },
            })
        )

    @classmethod
    def globalLexicalScopeNames(cls,
                                executionContextId: Optional['ExecutionContextId'] = None,
                                ):
        """Returns all let, const and class variables from global scope.
        :param executionContextId: Specifies in which execution context to lookup global scope variables.
        :type executionContextId: ExecutionContextId
        """
        return (
            cls.build_send_payload("globalLexicalScopeNames", {
                "executionContextId": executionContextId,
            }),
            cls.convert_payload({
                "names": {
                    "class": [],
                    "optional": False
                },
            })
        )

    @classmethod
    def queryObjects(cls,
                     prototypeObjectId: Union['RemoteObjectId'],
                     objectGroup: Optional['str'] = None,
                     ):
        """
        :param prototypeObjectId: Identifier of the prototype to return objects for.
        :type prototypeObjectId: RemoteObjectId
        :param objectGroup: Symbolic group name that can be used to release the results.
        :type objectGroup: str
        """
        return (
            cls.build_send_payload("queryObjects", {
                "prototypeObjectId": prototypeObjectId,
                "objectGroup": objectGroup,
            }),
            cls.convert_payload({
                "objects": {
                    "class": RemoteObject,
                    "optional": False
                },
            })
        )

    @classmethod
    def releaseObject(cls,
                      objectId: Union['RemoteObjectId'],
                      ):
        """Releases remote object with given id.
        :param objectId: Identifier of the object to release.
        :type objectId: RemoteObjectId
        """
        return (
            cls.build_send_payload("releaseObject", {
                "objectId": objectId,
            }),
            None
        )

    @classmethod
    def releaseObjectGroup(cls,
                           objectGroup: Union['str'],
                           ):
        """Releases all remote objects that belong to a given group.
        :param objectGroup: Symbolic object group name.
        :type objectGroup: str
        """
        return (
            cls.build_send_payload("releaseObjectGroup", {
                "objectGroup": objectGroup,
            }),
            None
        )

    @classmethod
    def runIfWaitingForDebugger(cls):
        """Tells inspected instance to run if it was waiting for debugger to attach.
        """
        return (
            cls.build_send_payload("runIfWaitingForDebugger", {
            }),
            None
        )

    @classmethod
    def runScript(cls,
                  scriptId: Union['ScriptId'],
                  executionContextId: Optional['ExecutionContextId'] = None,
                  objectGroup: Optional['str'] = None,
                  silent: Optional['bool'] = None,
                  includeCommandLineAPI: Optional['bool'] = None,
                  returnByValue: Optional['bool'] = None,
                  generatePreview: Optional['bool'] = None,
                  awaitPromise: Optional['bool'] = None,
                  ):
        """Runs script with given id in a given context.
        :param scriptId: Id of the script to run.
        :type scriptId: ScriptId
        :param executionContextId: Specifies in which execution context to perform script run. If the parameter is omitted the
evaluation will be performed in the context of the inspected page.
        :type executionContextId: ExecutionContextId
        :param objectGroup: Symbolic group name that can be used to release multiple objects.
        :type objectGroup: str
        :param silent: In silent mode exceptions thrown during evaluation are not reported and do not pause
execution. Overrides `setPauseOnException` state.
        :type silent: bool
        :param includeCommandLineAPI: Determines whether Command Line API should be available during the evaluation.
        :type includeCommandLineAPI: bool
        :param returnByValue: Whether the result is expected to be a JSON object which should be sent by value.
        :type returnByValue: bool
        :param generatePreview: Whether preview should be generated for the result.
        :type generatePreview: bool
        :param awaitPromise: Whether execution should `await` for resulting value and return once awaited promise is
resolved.
        :type awaitPromise: bool
        """
        return (
            cls.build_send_payload("runScript", {
                "scriptId": scriptId,
                "executionContextId": executionContextId,
                "objectGroup": objectGroup,
                "silent": silent,
                "includeCommandLineAPI": includeCommandLineAPI,
                "returnByValue": returnByValue,
                "generatePreview": generatePreview,
                "awaitPromise": awaitPromise,
            }),
            cls.convert_payload({
                "result": {
                    "class": RemoteObject,
                    "optional": False
                },
                "exceptionDetails": {
                    "class": ExceptionDetails,
                    "optional": True
                },
            })
        )

    @classmethod
    def setAsyncCallStackDepth(cls,
                               maxDepth: Union['int'],
                               ):
        """Enables or disables async call stacks tracking.
        :param maxDepth: Maximum depth of async call stacks. Setting to `0` will effectively disable collecting async
call stacks (default).
        :type maxDepth: int
        """
        return (
            cls.build_send_payload("setAsyncCallStackDepth", {
                "maxDepth": maxDepth,
            }),
            None
        )

    @classmethod
    def setCustomObjectFormatterEnabled(cls,
                                        enabled: Union['bool'],
                                        ):
        """
        :param enabled: 
        :type enabled: bool
        """
        return (
            cls.build_send_payload("setCustomObjectFormatterEnabled", {
                "enabled": enabled,
            }),
            None
        )

    @classmethod
    def setMaxCallStackSizeToCapture(cls,
                                     size: Union['int'],
                                     ):
        """
        :param size: 
        :type size: int
        """
        return (
            cls.build_send_payload("setMaxCallStackSizeToCapture", {
                "size": size,
            }),
            None
        )

    @classmethod
    def terminateExecution(cls):
        """Terminate current or next JavaScript execution.
Will cancel the termination when the outer-most script execution ends.
        """
        return (
            cls.build_send_payload("terminateExecution", {
            }),
            None
        )

    @classmethod
    def addBinding(cls,
                   name: Union['str'],
                   executionContextId: Optional['ExecutionContextId'] = None,
                   ):
        """If executionContextId is empty, adds binding with the given name on the
global objects of all inspected contexts, including those created later,
bindings survive reloads.
If executionContextId is specified, adds binding only on global object of
given execution context.
Binding function takes exactly one argument, this argument should be string,
in case of any other input, function throws an exception.
Each binding function call produces Runtime.bindingCalled notification.
        :param name: 
        :type name: str
        :param executionContextId: 
        :type executionContextId: ExecutionContextId
        """
        return (
            cls.build_send_payload("addBinding", {
                "name": name,
                "executionContextId": executionContextId,
            }),
            None
        )

    @classmethod
    def removeBinding(cls,
                      name: Union['str'],
                      ):
        """This method does not remove binding function from global object but
unsubscribes current runtime agent from Runtime.bindingCalled notifications.
        :param name: 
        :type name: str
        """
        return (
            cls.build_send_payload("removeBinding", {
                "name": name,
            }),
            None
        )



class BindingCalledEvent(BaseEvent):

    js_name = 'Runtime.bindingCalled'
    hashable = ['executionContextId']
    is_hashable = True

    def __init__(self,
                 name: Union['str', dict],
                 payload: Union['str', dict],
                 executionContextId: Union['ExecutionContextId', dict],
                 ):
        if isinstance(name, dict):
            name = str(**name)
        self.name = name
        if isinstance(payload, dict):
            payload = str(**payload)
        self.payload = payload
        if isinstance(executionContextId, dict):
            executionContextId = ExecutionContextId(**executionContextId)
        self.executionContextId = executionContextId

    @classmethod
    def build_hash(cls, executionContextId):
        kwargs = locals()
        kwargs.pop('cls')
        serialized_id_params = ','.join(['='.join([p, str(v)]) for p, v in kwargs.items()])
        h = '{}:{}'.format(cls.js_name, serialized_id_params)
        log.debug('generated hash = %s' % h)
        return h


class ConsoleAPICalledEvent(BaseEvent):

    js_name = 'Runtime.consoleAPICalled'
    hashable = ['executionContextId']
    is_hashable = True

    def __init__(self,
                 type: Union['str', dict],
                 args: Union['[RemoteObject]', dict],
                 executionContextId: Union['ExecutionContextId', dict],
                 timestamp: Union['Timestamp', dict],
                 stackTrace: Union['StackTrace', dict, None] = None,
                 context: Union['str', dict, None] = None,
                 ):
        if isinstance(type, dict):
            type = str(**type)
        self.type = type
        if isinstance(args, dict):
            args = [RemoteObject](**args)
        self.args = args
        if isinstance(executionContextId, dict):
            executionContextId = ExecutionContextId(**executionContextId)
        self.executionContextId = executionContextId
        if isinstance(timestamp, dict):
            timestamp = Timestamp(**timestamp)
        self.timestamp = timestamp
        if isinstance(stackTrace, dict):
            stackTrace = StackTrace(**stackTrace)
        self.stackTrace = stackTrace
        if isinstance(context, dict):
            context = str(**context)
        self.context = context

    @classmethod
    def build_hash(cls, executionContextId):
        kwargs = locals()
        kwargs.pop('cls')
        serialized_id_params = ','.join(['='.join([p, str(v)]) for p, v in kwargs.items()])
        h = '{}:{}'.format(cls.js_name, serialized_id_params)
        log.debug('generated hash = %s' % h)
        return h


class ExceptionRevokedEvent(BaseEvent):

    js_name = 'Runtime.exceptionRevoked'
    hashable = ['exceptionId']
    is_hashable = True

    def __init__(self,
                 reason: Union['str', dict],
                 exceptionId: Union['int', dict],
                 ):
        if isinstance(reason, dict):
            reason = str(**reason)
        self.reason = reason
        if isinstance(exceptionId, dict):
            exceptionId = int(**exceptionId)
        self.exceptionId = exceptionId

    @classmethod
    def build_hash(cls, exceptionId):
        kwargs = locals()
        kwargs.pop('cls')
        serialized_id_params = ','.join(['='.join([p, str(v)]) for p, v in kwargs.items()])
        h = '{}:{}'.format(cls.js_name, serialized_id_params)
        log.debug('generated hash = %s' % h)
        return h


class ExceptionThrownEvent(BaseEvent):

    js_name = 'Runtime.exceptionThrown'
    hashable = []
    is_hashable = False

    def __init__(self,
                 timestamp: Union['Timestamp', dict],
                 exceptionDetails: Union['ExceptionDetails', dict],
                 ):
        if isinstance(timestamp, dict):
            timestamp = Timestamp(**timestamp)
        self.timestamp = timestamp
        if isinstance(exceptionDetails, dict):
            exceptionDetails = ExceptionDetails(**exceptionDetails)
        self.exceptionDetails = exceptionDetails

    @classmethod
    def build_hash(cls):
        raise ValueError('Unable to build hash for non-hashable type')


class ExecutionContextCreatedEvent(BaseEvent):

    js_name = 'Runtime.executionContextCreated'
    hashable = ['contextId']
    is_hashable = True

    def __init__(self,
                 context: Union['ExecutionContextDescription', dict],
                 ):
        if isinstance(context, dict):
            context = ExecutionContextDescription(**context)
        self.context = context

    @classmethod
    def build_hash(cls, contextId):
        kwargs = locals()
        kwargs.pop('cls')
        serialized_id_params = ','.join(['='.join([p, str(v)]) for p, v in kwargs.items()])
        h = '{}:{}'.format(cls.js_name, serialized_id_params)
        log.debug('generated hash = %s' % h)
        return h


class ExecutionContextDestroyedEvent(BaseEvent):

    js_name = 'Runtime.executionContextDestroyed'
    hashable = ['executionContextId']
    is_hashable = True

    def __init__(self,
                 executionContextId: Union['ExecutionContextId', dict],
                 ):
        if isinstance(executionContextId, dict):
            executionContextId = ExecutionContextId(**executionContextId)
        self.executionContextId = executionContextId

    @classmethod
    def build_hash(cls, executionContextId):
        kwargs = locals()
        kwargs.pop('cls')
        serialized_id_params = ','.join(['='.join([p, str(v)]) for p, v in kwargs.items()])
        h = '{}:{}'.format(cls.js_name, serialized_id_params)
        log.debug('generated hash = %s' % h)
        return h


class ExecutionContextsClearedEvent(BaseEvent):

    js_name = 'Runtime.executionContextsCleared'
    hashable = []
    is_hashable = False

    def __init__(self):
        pass

    @classmethod
    def build_hash(cls):
        raise ValueError('Unable to build hash for non-hashable type')


class InspectRequestedEvent(BaseEvent):

    js_name = 'Runtime.inspectRequested'
    hashable = []
    is_hashable = False

    def __init__(self,
                 object: Union['RemoteObject', dict],
                 hints: Union['dict', dict],
                 ):
        if isinstance(object, dict):
            object = RemoteObject(**object)
        self.object = object
        if isinstance(hints, dict):
            hints = dict(**hints)
        self.hints = hints

    @classmethod
    def build_hash(cls):
        raise ValueError('Unable to build hash for non-hashable type')
