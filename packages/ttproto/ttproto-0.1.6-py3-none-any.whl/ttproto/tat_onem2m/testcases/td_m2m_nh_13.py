from ..common import *


class TD_m2m_nh_13 (CoAPTestCase):
    """
---
TD_M2M_NH_13:
    cfg: M2M_CFG_01
    obj: AE deletes a specific container resource via a container DELETE Request
    pre: AE has created an Application Entity resource <AE> on Registrar CSE and
         AE has created a container resource <container> on Registrar CSE.
    ref: 'TS-0001, clause 10.2.4.4 and TS-0004, clause 7.3.5.2.4'
    seq:
    -   s:
        - 'AE is requested to send a <container> Delete Request:'
        -   - Type = 0 (CON)
            - Code = 4 (DELETE)
    -   c:
        - 'The request sent by the client contains:'
        -   - Type=0 and Code=4
            - "Client-generated Message ID (\u2794 CMID)"
            - "Client-generated Token (\u2794 CTOK)"
            - oneM2M-FR=AE-ID
            - oneM2M-RQI=token-string (CRQI)
            - Empty payload
    -   v: Check if possible that the <container> resource is deleted in registrar CSE
    -   c:
        - 'Registrar CSE sends response containing:'
        -   - Code = 2.02 (OK)
            - Message ID = CMID, Token = CTOK
            - Empty Payload
            - oneM2M-RSC=2002
            - oneM2M-RQI=CRQI
    -   v: Check if possible that the <AE> resource has been removed from registrar CSE
    -   v: AE indicates a successuful operation
    """

    @classmethod
    @typecheck
    def get_stimulis(cls) -> list_of(Value):
        """
        Get the stimulis of this test case. This has to be be implemented into
        each test cases class.

        :return: The stimulis of this TC
        :rtype: [Value]
        """
        return [CoAP(type='con', code='delete')]

    def run(self):
        
        self.match('client', CoAP(type='con', code='delete', pl=(b'')), 'fail')
        self.match('client', CoAP(opt=Opt(CoAPOptionOneM2MFrom())), 'fail')
        if self.match('client', CoAP(opt=Opt(CoAPOptionOneM2MRequestIdentifier())), 'fail'): 

            CMID = self.coap['mid']
            CTOK = self.coap['tok']
            OPTS = self.coap['opt']
            RI = OPTS[CoAPOptionOneM2MRequestIdentifier]
            RIVAL = RI[2]

            self.next()

            self.match('server', CoAP(code=2.02, mid=CMID, tok=CTOK, pl=(b'')), 'fail')
            self.match('server', CoAP(opt=Opt(CoAPOptionOneM2MResponseStatusCode('2002'))), 'fail')
            self.match('server', CoAP(opt=Opt(CoAPOptionOneM2MRequestIdentifier(RIVAL))), 'fail')
