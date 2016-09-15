"""
Project mesh onto another mesh non-destructive
http://www.fevrierdorian.com/blog/post/2011/07/31/Project-a-mesh-to-another-with-Maya-API-(English-Translation)

import maya.cmds as cmds

cmds.loadPlugin( "F:/git/Maya/mayascripts/projectMesh.py" );
node = cmds.createNode('projectMesh')
cmds.connectAttr('{}.outputMesh'.format(node), 'pSphereShape2.inMesh')
cmds.connectAttr('pPlaneShape1.worldMesh[0]', '{}.inputMeshSrc'.format(node))
cmds.connectAttr('pSphereShape1.worldMesh[0]', '{}.inputMeshTarget'.format(node))

cmds.delete(node)
cmds.flushUndo()
cmds.unloadPlugin("projectMesh")
"""

import sys

import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

kPluginNodeType = "projectMesh"
kPluginNodeId = om.MTypeId(0x80000)


# node definition
class projectMeshNode(ompx.MPxNode):

    inputMeshSrc = om.MObject()
    inputMeshTarget = om.MObject()
    outputMesh = om.MObject()

    # constructor
    def __init__(self):

        ompx.MPxNode.__init__(self)

    def compute(self, plug, data):

        if not plug == self.outputMesh:
            return om.kUnknownParameter

        # get the inputmeshtarget (return MDataHandle)
        inMeshSrcHandle = data.inputValue(self.inputMeshSrc)
        inMeshTargetHandle = data.inputValue(self.inputMeshTarget)

        if not inMeshSrcHandle.type() == om.MFnData.kMesh or not inMeshTargetHandle.type() == om.MFnData.kMesh:
            return om.kInvalidParameter

        # return a MObject
        meshSrc = inMeshSrcHandle.asMesh()
        meshTarget = inMeshTargetHandle.asMesh()

        # get MFnMesh
        mFnMeshSrc = om.MFnMesh(meshSrc)
        mFnMeshTarget = om.MFnMesh(meshTarget)

        outputMeshMPointArray = om.MPointArray()
        mFnMeshSrc.getPoints(outputMeshMPointArray)

        # get MDagPath of the MMesh to get the MMatrix and multiply vertext to it
        inMeshSrcMDagPath= mFnMeshSrc.dagPath()     # MDagPath
        inMeshSrcInclusiveMatrix = inMeshSrcMDagPath.inclusiveMatrix()      # MMatrix

        for i in range( outputMeshMPointArray.length()):

            inMeshMPointTmp = outputMeshMPointArray[i] * inMeshSrcInclusiveMatrix # the MPoint of the meshSrc in the worldspace

            rayDirection = om.MVector()

            raySource = om.MFloatPoint(inMeshMPointTmp.x, inMeshMPointTmp.y, inMeshMPointTmp.z)
            mFnMeshSrc.getVertexNormal(i, False, rayDirection)
            rayDirection *= inMeshSrcInclusiveMatrix
            rayDirection = om.MFloatVector(rayDirection.x, rayDirection.y, rayDirection.z)


            hitPoint = om.MFloatPoint()

            # rest of the args
            hitFacePtr = om.MScriptUtil().asIntPtr()
            idsSorted = False
            testBothDirections = False
            faceIds = None
            triIds = None
            accelParams = None
            hitRayParam = None
            hitTriangle = None
            hitBary1 = None
            hitBary2 = None
            maxParamPtr = 9999999

            hit =mFnMeshTarget.closestIntersection(raySource,
                                                   rayDirection,
                                                   faceIds,
                                                   triIds,
                                                   idsSorted,
                                                   om.MSpace.kWorld,
                                                   maxParamPtr,
                                                   testBothDirections,
                                                   accelParams,
                                                   hitPoint,
                                                   hitRayParam,
                                                   hitFacePtr,
                                                   hitTriangle,
                                                   hitBary1,
                                                   hitBary2)

            if hit:
                inMeshMPointTmp = om.MPoint(hitPoint.x, hitPoint.y, hitPoint.z)
                outputMeshMPointArray.set(inMeshMPointTmp, i)

        newDataCreator = om.MFnMeshData()

        newOutputData = newDataCreator.create()     # MObject

        outMeshNumVtx = mFnMeshSrc.numVertices()
        outMeshNumPolygons = mFnMeshSrc.numPolygons()

        # create two arrays and feed them
        outMeshPolygonCountArray = om.MIntArray()
        outMeshVtxArray = om.MIntArray()

        mFnMeshSrc.getVertices(outMeshPolygonCountArray, outMeshVtxArray)

        # now create the mesh
        meshFS = om.MFnMesh()
        meshFS.create(outMeshNumVtx,
                      outMeshNumPolygons,
                      outputMeshMPointArray,
                      outMeshPolygonCountArray,
                      outMeshVtxArray,
                      newOutputData)

        # store the mesh on the output plug
        outputMeshHandle = data.outputValue(self.outputMesh)
        outputMeshHandle.setMObject(newOutputData)

        # clean data
        data.setClean(plug)




def nodeCreator():
    return ompx.asMPxPtr(projectMeshNode())


# initializer
def nodeInitializer():
    typedAttr = om.MFnTypedAttribute()

    # setup the input attributes
    projectMeshNode.inputMeshSrc = typedAttr.create("inputMeshSrc",
                                                    "inputMeshSrc",
                                                    om.MFnData.kMesh)
    typedAttr.setReadable(False)
    projectMeshNode.addAttribute(projectMeshNode.inputMeshSrc)

    projectMeshNode.inputMeshTarget = typedAttr.create("inputMeshTarget",
                                                       "inputMeshTarget",
                                                       om.MFnData.kMesh)
    typedAttr.setReadable(False)
    projectMeshNode.addAttribute(projectMeshNode.inputMeshTarget)

    # setup the output attribute
    projectMeshNode.outputMesh = typedAttr.create("outputMesh",
                                                  "outputMesh",
                                                  om.MFnData.kMesh)
    typedAttr.setWritable(False)
    typedAttr.setStorable(False)
    projectMeshNode.addAttribute(projectMeshNode.outputMesh)

    # Set the attribute dependencies
    projectMeshNode.attributeAffects(projectMeshNode.inputMeshSrc, projectMeshNode.outputMesh)
    projectMeshNode.attributeAffects(projectMeshNode.inputMeshTarget, projectMeshNode.outputMesh)




# initialize the script plugin-in
def initializePlugin(mObject):

    mplugin = ompx.MFnPlugin(mObject)

    try:
        mplugin.registerNode(kPluginNodeType,
                             kPluginNodeId,
                             nodeCreator,
                             nodeInitializer)
    except:
        sys.stderr.write('Failed to register node: {}'.format(kPluginNodeType))
        raise


# unintialize the script plug-in
def uninitializePlugin(mObject):
    mplugin = ompx.MFnPlugin(mObject)
    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        sys.stderr.write("Failed to register node: {}".foramt(kPluginNodeType))
        raise


