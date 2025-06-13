The interactive RunJob API provides an interface for user to work with Rodan. There are two APIs for this functionality:

````
/interactive/RunJob_UUID/acquire/
/interactive/RunJob_UUID/Token/(sub URL)
````

The idea behind is that the user has to acquire a "lock" before they start working on an interactive RunJob. This is done through the first API (`acquire`). The acquisition, if successful, only ensures a certain seconds of the user's lock, and thus the Rodan client has to extend the lock before the previous one expires. The `acquire` API, if successful, returns a token and expiry time.

Using the token, the user then accesses the second API to retrieve the interactive interface. Rodan supports sub-URLs for sub interfaces and Ajax purposes. At last, the user sends a POST to store the result of the interactive RunJob.

A recommended client UX design is to load the interactive interface as an `<iframe>` while keeping `POSTing` the `acquire` API in the background.

[[images/client_interactive_runjob_interface.png]]

You may also be interested in the following class, written by Andrew Fogarty for the Interactive Classifier (https://github.com/DDMAL/Interactive-Classifier). Please note that it requires jQuery and is written in ECMAScript 6.

```
import $ from "jquery";

/**
 * This class maintains a `runjob.working_user_expiry` Rodan token throughout its lifetime.
 *
 * For more information, see {@link https://github.com/DDMAL/Interactive-Classifier/wiki/Token-Authentication}.
 */
export default class Authenticator {

    /**
     * Grabs the authentication URL from the page URL and sets the timeout
     * to 5000 miliseconds.
     */
    constructor()
    {
        // This will be the URL that we hit to authenticate.
        this._authUrl = Authenticator.getAuthUrl();
        // Authenticate every few seconds
        this._time = 5000;
    }

    /**
     * Start authenticating on an interval.
     */
    startTimedAuthentication()
    {
        var that = this;
        this._timer = setInterval(function ()
        {
            that.authenticate();
        }, this._time);
    }

    /**
     * Authenticate with the server then save the working POST url for when
     * we will submit to the server later.
     */
    authenticate()
    {
        var that = this;
        $.ajax({
            url: this._authUrl,
            type: 'POST',
            headers: {
                Accept: "application/json; charset=utf-8",
                "Content-Type": "application/json; charset=utf-8"
            },
            complete: function (response)
            {
                var responseData = JSON.parse(response.responseText);
                // Save the working url
                that._workingUrl = responseData["working_url"];
            }
        });
    }

    /**
     * Get the working POST url for the Interactive Job.  This is the URL that
     * we make a post request to when we want to complete the interactive
     * portion of the interactive job.
     *
     * @returns {string} - The "working" URL on the server for the job.
     */
    getWorkingUrl()
    {
        return this._workingUrl;
    }

    /**
     * Get the authentication url.
     *
     * @returns {string} - The authentication URL.
     */
    static getAuthUrl()
    {
        return window.location.href.split("/").slice(0, -2).join("/") + "/acquire/";
    }
}
```