[![Build Status](https://api.travis-ci.org/uw-it-aca/django-aws-message.svg?branch=master)](https://travis-ci.org/uw-it-aca/django-aws-message)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/django-aws-message/badge.png?branch=master)](https://coveralls.io/r/uw-it-aca/django-aws-message?branch=master)

ACA AWS SNS/SQS Message App
===========================

A Django Application on which to build AWS SNS endpoints and SQS gatherers

Installation
------------

**Project directory**

Install django-aws-message in your project.

    $ cd [project]
    $ pip install django-aws-message

Project settings.py
------------------

**AWS App settings**

     # AWS SQS gather app
     AWS_SQS = {
         'ENROLLMENT' : {
             'TOPIC_ARN' : 'arn:aws:sqs:...',
             'QUEUE': 'some:specific:queue:id',
             'REGION': '<queue's amazon region label>',
             'ACCOUNT_NUMBER': '<queue's amazon account number>',
             'KEY_ID': '<lograndomlookingstring>',
             'KEY': '<longerrandomlookingstring>',
             'VISIBILITY_TIMEOUT': 60,
             'MESSAGE_GATHER_SIZE': 10,
             'VALIDATE_SNS_SIGNATURE': True,
             'VALIDATE_MSG_SIGNATURE': True,
             'PAYLOAD_SETTINGS': {}
         }
     }
