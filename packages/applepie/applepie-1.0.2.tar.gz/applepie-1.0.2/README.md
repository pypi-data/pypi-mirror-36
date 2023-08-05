# applepie
This is a Python library for decrypting Apple Pay tokens on the server side.

# Reference
https://developer.apple.com/library/ios/documentation/PassKit/Reference/PaymentTokenJSON/PaymentTokenJSON.html

# Installation

First, simply applepie via pip, like usual

```sh
$ pip install applepie
```

In order to use this library, you will need 3 files:

1. Apple's root certificate. This is included in the library, but you could reference your own version if it if you don't trust the one in the library.
  * [Download from Apple's Certificate Authority Repository](https://www.apple.com/certificateauthority/)
  * OR `wget https://www.apple.com/certificateauthority/AppleRootCA-G3.cer`
2. Your certificate, downloadable from the [Apple Developer Center](https://developer.apple.com/account/).
3. Your private key, downloadable from the [Apple Developer Center](https://developer.apple.com/account/).

If you don't have a certificate and private key from the Apple Developer Center, follow all of the instructions in the [Apple Pay setup documentation](https://developer.apple.com/documentation/passkit/apple_pay/setting_up_apple_pay_requirements).

When you are using these certificates, you can either use file paths to reference them, or you can choose to read their contents into a variable and pass that. If you are running a [Twelve-Factor App](https://12factor.net/) or simply would prefer to keep the certificates in an environment variable, you can do that.


## Usage

```python
import applepie

# Load in the merchant certificate and private key.
# Optionally, you could just set the paths instead of opening them manually here.
certificate = open("apple_pay.cer", "rb").
private_key = open("private_key.key", "rb").read()
root_certificate = open("AppleRootCA-G3.cer", "rb").read()

# Note: payment is expected to be the paymentData element from Apple's documentation.
# It should have data, header, signature, and version as keys
parser = applepie.Parser(dataset)
token = parser.decrypt(certificate, private_key, root_certificate)

# Optionally, you could call it like this instead
# token = parser.decrypt("./path/to/apple_pay.cer", "./path/to/private_key.key")

# token is an applepie Token, which is a class that facilitates parsing of the data response from Apple
# token.data - Raw response from Apple.
# token.card_holdername - Cardholder name. Can be blank.
# token.card_number - Card number to charge
# token.expiration_date - datetime.datetime object. This defaults to 23:59:59.999 for the time part.
# token.amount - moneyed.Money() object in the proper currency. See py-moneyed for details.
# token.manufacturer - Device manufacturer (usually not used)
# token.payment_data_type - 3DSecure normally, but can be EMV if you are in China
# token.paymentData - JSON blob of detailed payment data. See Apple's PaymentToken reference for detail.

# token.data example
# 
# {
#   "applicationPrimaryAccountNumber"=>"4804123456789012",
#   "applicationExpirationDate"=>"190123",
#   "currencyCode"=>"123",
#   "transactionAmount"=>700,
#   "deviceManufacturerIdentifier"=>"123456789012",
#   "paymentDataType"=>"3DSecure",
#   "paymentData"=> {
#     "onlinePaymentCryptogram"=>"<<Base64EncodedData>>",
#     "eciIndicator"=>"5"
#   }
# }

```
