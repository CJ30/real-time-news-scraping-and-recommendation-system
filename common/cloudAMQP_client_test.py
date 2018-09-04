from cloudAMQP_client import CloudAMQPClient

# TODO: use your own queue url.
CLOUDAMQP_URL = "amqp://goelcjlr:3QhYAab5gLp6u3mT03ZYFRaq3kyq2pmF@donkey.rmq.cloudamqp.com/goelcjlr"
NEWS_FETCH_TASK_QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, NEWS_FETCH_TASK_QUEUE_NAME)

    sentMsg = {'test':'test'}
    client.sendMessage(sentMsg)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed.'

if __name__ == "__main__":
    test_basic()
