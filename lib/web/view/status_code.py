#!/usr/bin/python
# -*- coding: utf-8 -*-

CODE = "code"
MESSAGE = "message"


class STATUS_CODE:

    class BAD_ARGUMENT:
        code = 999
        msg = "Bad Argument"

    class LOGIN_REQUIRED:

        """需要登录.
        """
        code = 1000
        msg = "Login required"

    class USERNAME_EXISTED:
        code = 1001
        msg = "Username existed"

    class USERNAME_EMPTY:
        code = 1002
        msg = "Username is empty"

    class USER_NOT_EXIST:
        code = 1003
        msg = "User doesn't exist"

    class USER_BLOCKED_BY_ADMIN:

        '''用户被禁止某些操作.
        '''
        code = 1004
        msg = "User blocked by administrator"

    class USER_DISABLED:

        """用户被禁止登陆.
        """
        code = 1005
        msg = "User disabled by administrator"

    class USERNAME_ILLEGAL:
        code = 1006
        msg = "invalid username"

    class USER_NOT_FOLLOWED:

        """unfollow的时候, 如果用户没有follow对方.
        """
        code = 1007
        msg = "You have not followed this user"

    class CAN_NOT_FOLLOW_YOURSELF:
        code = 1008
        msg = "Cannot follow yourself"

    class USER_ALREADY_FOLLOWED:

        """试图follow一个已经follow了的用户.
        """
        code = 1009
        msg = "Already followed this user"

    class USER_IS_BLOCKED:
        code = 1010
        msg = "User has been blocked"

    class OPERATION_NOT_PERMIT:

        """用户试图进行其没有权限进行的操作.
        """
        code = 1011
        msg = "Operation forbidden"

    class USER_CAN_NOT_CHAT:
        code = 1012
        msg = "User cannot chat"

    class USER_ACTION_DONE:

        """当客户端在时间间隔内重复调用/user/action接口是抛出
        """
        code = 1013
        msg = "Already done this action"

    class USER_ACTION_UNKNOW:

        """当客户端传的action_type不合法时抛出
        """
        code = 1014
        msg = "Action unknown"

    class RegisterInfoNotSatisfy:
        code = 10151
        msg = "register error: "

    class LoginInfoNotSatisfy:
        code = 10152
        msg = "login error: "

    class PHONE_ALREADY_REGISTED:
        code = 1015
        msg = "Phone already registed"

    class NICKNAME_TOO_LONG:
        code = 1016
        msg = "Nickname too long"

    class PASSWORD_TOO_SIMPLE:
        code = 1017
        msg = "Password too simple"

    class PASSWORD_NOT_MATCH:
        code = 1018
        msg = "Passwords not match"

    class Password_Diff:
        code = 6001
        msg = "New Password diff Confirm Password"

    class ACCOUNT_NOT_EXISTS:
        code = 1019
        msg = "Account not exists"

    class USER_CAN_NOT_BORADCAST:

        """用户被管理员禁止直播.
        """
        code = 1020
        msg = 'User broadcast disabled by admin'

    class USER_LEVEL_NOT_ENOUGH_BORADCAST:

        """用户等级不够开启直播.
        """
        code = 1021
        msg = {
            "TH":"คุณจำเป็นที่จะต้องผ่าน Level %s ก่อนถึงจะสามารถออนแอร์ได้",
            "EN":"Level %s is required to start a broadcast"
        }

    class LIVE_NOT_FOUND:
        code = 2000
        msg = "Live not found"

    class LIVE_STATUS_NOT_SATISFY:
        code = 2001
        msg = "Live status not satisfy"

    # 由于某些特殊原因不能够让用户开启直播
    class LIVE_CAN_NOT_START:
        code = 2002
        msg = "Live can not start"

    class LIVE_HOST_TEMPORARY_LEAVE:
        code = 2003
        msg = "Host temporary leave"

    class LIVE_HOST_ONLY_OPERATE:
        code = 2004
        msg = "Only live host can operate"

    class GIFT_NOT_FOUND:
        code = 3000
        msg = "Gift not found"

    class GIFT_NOT_AVAILABLE:
        code = 3001
        msg = "Gift not available"

    class INSUFFICIENT_BALANCE:
        code = 3002
        msg = "insufficient balance"

    class CAN_NOT_SEND_GIFT_TO_YOURSELF:
        code = 3003
        msg = "Can not send gift to yourself"


    class HURRY_GIFT_NOT_AVAILABLE:
        code = 3004
        msg = "Hurry gift not available"


    class CAN_NOT_SEND_GUARD_GIFT:
        code = 3005
        msg = "Can not send guard gift"


    class SIGNATURE_VERIFY_FAIL:
        code = 4000
        msg = "Signature verify fail"

    class PURCHASE_VERIFY_FAIL:
        code = 4001
        msg = "Purchase verify fail"

    class PRODUCT_ID_DUPLICATED:
        code = 4002
        msg = "Product id duplicated"

    class BILL_INTERFACE_UNKNOW:
        code = 4003
        msg = "Bill interface unknow"

    class BILL_ORDER_TYPE_UNKONW:
        code = 4004
        msg = "Bill order_type unkonw"

    class PRODUCT_NOT_FOUND:
        code = 4005
        msg = "Product not found"

    class PRODUCI_NOT_AVAILABLE:
        code = 4006
        msg = "Product not available"

    class UNKNOW_GOOGLE_PAYMENT_ERROR:
        code = 4007
        msg = "unknow google payment error"

    class PURCHASE_CANCELLED:
        code = 4008
        msg = "Purchase cancelled"

    class BILL_NOT_MATCH:
        code = 4009
        msg = "Bill not match"

    class BILL_NOT_FOUND:
        code = 4010
        msg = "Bill not found"

    class BILL_PAYLOAD_NOT_MATCH:
        code = 4011
        msg = "Bill payload not match"

    class BILL_STATUS_NOT_SATISFY:
        code = 4012
        msg = "Bill status not satisfy"

    class BILL_INTERFACE_ORDER_ID_DUPLICATED:
        code = 4013
        msg = "Bill interface order id duplicated"

    class BILL_APPLE_STORE_CHECK_FAIL:
        code = 4014
        msg = "Apple store check fail"

    class BILL_APPLE_TRANSACTION_ID_NOT_FOUND:
        code = 4015
        msg = "Apple transction id not found"

    class BILL_NOT_SUCCEED:
        code = 4016
        msg = "Bill Not succeed"

    class BAD_PHONE_NUMBER:
        code = 5000
        msg = "Bad phone number"

    class SEND_SMS_FAIL:
        code = 5001
        msg = "SMS send fail"

    class SMS_VERIFY_FAIL:
        code = 5002
        msg = "SMS verify fail"

    class SEND_SMS_OUT_OF_QUOTA:
        code = 5003
        msg = "SMS out of quota"

    class TOKEN_ILLEGAL:
        code = 5004
        msg = "Token illegal"

    class DEVICE_NOT_TOKEN:
        code = 5005
        msg = "no device token"

    class NO_AUTHORIZATION_CODE:
        code = 5006
        msg = "no authorization code"

    class PAYPAL_PAY_FAIL:
        code = 5007
        msg = "paypal pay fail"

    class CODAPAY_FAIL:
        code = 5007
        msg = "coda pay fail"
    # 6000的异常码是非致命异常

    class PAY_NO_FIRST_RECHARGE:
        code = 5008
        msg = "no first recharge"

    class RECHARGE_LIMIT:
        code = 5009
        msg = "recharge limit"

    class FCM_SUBSCRIBE_TOPIC_FAIL:
        code = 6000
        msg = "FCM subscribe topic fail"

    class EVENT_NOT_FOUND:
        code = 6001
        msg = "Event Not Found"

    class EVENT_NOT_START:
        code = 6002
        msg = "Event Not Start Yet"

    class EVENT_IS_END:
        code = 6003
        msg = "Event Is End"

    class EVENT_HAS_APPLY:
        code = 6004
        msg = 'Event has apply'

    class LINE_PAY_REQUEST_FAIL:
        code = 6005
        msg = 'Request has failed'

    class LINE_PAY_CONFIRM_FAIL:
        code = 6006
        msg = 'Line pay confirm failed'

    class LINE_PAY_RESERVE_FAIL:
        code = 6007
        msg = 'Line pay reserve failed'

    class TASK_NOT_FOUND:
        code = 3000
        msg = "task not found"

    class GUIDE_ACTIVITY_NOT_FOUND:
        code = 7000
        msg = "guide activity not found"

    class MSG_TYPE_NOT_FOUND:
        code = 8000
        msg = "msg type not found"

    class MSG_PUBLIC_TYPE_NOT_FOUND:
        code = 8001
        msg = "msg public type not found"

    class UNIPIN_REQUEST_FAILURE:
        code = 10000
        msg = "unipin request failure, request code = "

    class UNIPIN_HTTP_FAILURE:
        code = 10001
        msg = "unipin http request failure."

    class BROADCAST_NOT_DISABLED:
        code = 9001
        msg = "broadcast not disabled"

    class PACKET_IS_EMPTY:
        code = 11001
        msg = "The redpacket is empty."

    class PACKET_GOT:
        code = 11002
        msg = "You have got the redpacket."

    class PACKET_NOT_FOUND:
        code = 11003
        msg = "The redpacket is not found."

    class PACKET_INCORRECT:
        code = 11004
        msg = "Incorrect redpacket size or ruby."

    class PRIVILEGE_TOO_LOW:
        code = 9100
        msg  = "privilege too tow"

    class LEVEL_NOT_ENOUGH_PRIVILEGE:
        code = 9101
        msg  = "level not enough privilege"


    class PRIVILEGE_MATERIAL_NOT_FOUND:
        code = 9102
        msg  = "privilege material not found"


    class INVITATION_NOT_FOUND:
        code = 12001
        msg  = "invitation not found."


    class INVITATIONRELATION_EXIST:
        code = 12002
        msg  = "invitation relation exists."


    class INVALID_INVITATIONRELATION:
        code = 12003
        msg  = "invalid invitation relation."


    class BALANCE_COIN_INSUFFICIENT:
        code = 13000
        msg  = "user balance coin not enough"


    class USER_WEEK_WITHDRAW:
        code = 13001
        msg  = "user have withdraw weekly"


    class ACCOUNTINFO_IMPERFECT:
        code = 13002
        msg  = "account info imperfect"


    class SIGN_REWARD_NOT_FOUND:
        code = 14000
        msg  = "sign failed"


    class SIGN_GAINED:
        code = 14001
        msg  = "you have signed"

    class BID_BUSY:
        code = 15001
        msg  = "Someone is bidding for the host, please wait in order."

    class BID_FAILED:
        code = 15002
        msg  = "Bid failed."

