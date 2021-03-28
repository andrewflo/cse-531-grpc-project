from concurrent import futures

import grpc

import branch_pb2
import branch_pb2_grpc


class Branch(branch_pb2_grpc.BranchServicer):
    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()

    def MsgDelivery(self, request, context):
        result = "success"

        if request.money < 0:
            result = "fail"
        elif request.interface == "query":
            pass
        elif request.interface == "deposit":
            self.balance += request.money
        elif request.interface == "withdraw":
            if self.balance >= request.money:
                self.balance -= request.money
            else:
                result = "fail"
        else:
            result = "fail"

        return branch_pb2.MsgResponse(interface=request.interface, result=result, money=self.balance)

    def Propagate_Withdraw(self):
        pass

    def Propagate_Deposit(self):
        pass