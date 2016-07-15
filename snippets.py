import maya.cmds as cmds
import maya.OpenMaya as om


def jointInCentre():
    """
    Takes a selection and creates a joint in the middle of it. Works with
    selection of vertices or edges

    :return:
    """

    print 'Putting a joint in the centre of a selection!'

    selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selection)

    iterSel = om.MItSelectionList(selection)

    posX = []
    posY = []
    posZ = []

    while not iterSel.isDone():

        mObj = om.MObject()
        mDagpath = om.MDagPath()

        iterSel.getDagPath(mDagpath, mObj)

        #print mObj.apiTypeStr()
        #print mObj.apiType()

        if mObj.hasFn(om.MFn.kMeshVertComponent):
            mVertIter = om.MItMeshVertex(mDagpath, mObj)

            print "We have {0} vertices selected".format(mVertIter.count())
            mVertIter.reset()

            while not mVertIter.isDone():
                vertPoint = mVertIter.position(om.MSpace.kWorld)
                print vertPoint.x, vertPoint.y, vertPoint.z

                posX.append(vertPoint.x)
                posY.append(vertPoint.y)
                posZ.append(vertPoint.z)

                mVertIter.next()
        elif mObj.hasFn(om.MFn.kMeshEdgeComponent):

            mEdgeIter = om.MItMeshEdge(mDagpath, mObj)
            print "We have {0} edges selected".format(mEdgeIter.count())

            vertIndices = []

            mEdgeIter.reset()
            while not mEdgeIter.isDone():

                for i in range(2):
                    if not mEdgeIter.index(1) in vertIndices:

                        point = mEdgeIter.point(i, om.MSpace.kWorld)

                        posX.append(point.x)
                        posY.append(point.y)
                        posZ.append(point.z)

                        vertIndices.append(mEdgeIter.index(i))

                mEdgeIter.next()

        else:
            print 'Selection is not a vertices or edges!'

        ##########################################
        # Do not comment this out!!!!
        iterSel.next()


    centreX = sum(posX) / len(posX)
    centreY = sum(posY) / len(posY)
    centreZ = sum(posZ) / len(posZ)

    print 'Centre point is: {0} {1} {2}'.format(centreX, centreY, centreZ)

    cmds.select(clear=True)
    cmds.joint(position=[centreX,centreY, centreZ])

