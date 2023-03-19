

## Instructions
Before we get started, create an application on Smartcar's Developer Dashboard to get your API keys.

**Note:** On the dashboard, you will want to set your `redirect_uri` as `https://car-charging.herokuapp.com/exchange`.

Then, we can set these as environment variables -
```bash
$ export SMARTCAR_CLIENT_ID=<your-client-id>
$ export SMARTCAR_CLIENT_SECRET=<your-client-secret>
$ export SMARTCAR_REDIRECT_URI=https://car-charging.herokuapp.com/exchange
```

Make sure you have cloned this repo -
```bash
$ git clone https://github.com/smartcar/getting-started-python-sdk.git
$ cd getting-started-python-sdk/app
```




To install the required dependencies and run this Python app -
```bash
$ pip install -r requirements.txt
$ python main.py
```

Once your server is up and running, you can authenticate your vehicle. In our current set up, we are using Smartcar's [test mode](https://smartcar.com/docs/guides/testing/), so you can log in with any username and password. To authenticate, navigate to `https://car-charging.herokuapp.com/login`. Once you have authenticated, go to `https://car-charging.herokuapp.com/vehicle` to see your vehicle information.




