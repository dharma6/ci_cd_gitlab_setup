## Credit goes to Brad Beggs : https://www.linkedin.com/in/bradleybeggs/. 
This is primarly designed for our work place CI-CD setup, and it was setup by Brad. I just helped him in testing the end-end of the following CI-CD in one of our project which helped us to discover new things. 

-----------------
## First Step - Install Serverless & Plugins
First, install Serverless (SLS) globally so you can use the SLS CLI commands. 

If you have SLS already installed, you might need to update it to ^2.43.0 or higher 

```bash
npm install -g serverless   
#  or
npm update serverless -g 
```

Install the (SLS) plugins. 
```bash
npm install
```

Once everything is installed, you can use SLS locally. 

\
&nbsp;

-----------------
## Second Step - Write Lambdas & Use apiResponse
Open the repo and add your lambdas in the `/lambdas` folder. 

`Note:` You can internally structure the `/lambdas` folder however you like. But the main handler function must be in `/lambdas/` and not a sub directory.

If you don't use this folder, the pipeline and deployment will fail.   
  \
&nbsp;
### API Gateway Responses (optional)
Handle API responses easily (and automatically) with the API response class. 

The class is found here: `./lambdas/api/apiResponses.py` 

You write your custom return message, and the API class automatically includes pre-arranged status code (`200, 400`, etc), and all needed return headers. 

 Each `response._classMethod()` expects a single parameter as an object. For example:

```
response._200( {"message": "Not a valid API-Key"} )
```

The `response._200()` can be used like this:

 ```python
 # in the handler.py, for example

from lambdas.api.apiResponses import *   # import the class

response = API()  # create the class API instance 

if(validate_api_key_response == False):
        return response._200 (  
            {"message": "Not a valid API-Key"}
        )
```

`Note:` If you do not need `./api`, please delete the whole folder.   
\
&nbsp;
### Using Imported Modules & Requirements.txt
Add any python packages/modules in `requirements.txt`.

These packages will get bundled by SLS automatically and deployed to AWS Lambda. 

**Delete `requirements.txt` if you are not using it. Otherwise a docker image is built unnecessarily.** 

\
&nbsp;
\
&nbsp;

-----------------

## Third Step - Develop & Run Locally and/or on AWS

### How to Test Locally

```bash
sls invoke local --function theSLSFunctionName
```

To test a lambda with string data, use the `--data <stringOfDataHere>` flag. For example:
```bash
sls invoke local --function theSLSFunctionName --data <stringOfDataHere>
```  

To test a lambda with an `json` object, create a `.json` file in `./lambdas/testData` and create your `json` object there and use `--path relativePathSourceHere`. For example:


```bash
sls invoke local --function theSLSFunctionName --path lambdas/testData/demoTestData.json
```  

[See this link for how to other data items](https://www.serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/)  
\
&nbsp;


### How to Deploy To AWS Lambda Directly  
To test your Lambda you can deploy from your CLI to AWS; SLS handles the packaging/zip for you.  
\
&nbsp;

#### **Deploy Everything Once**
Deploy the lambda function package with verbose (`-v`) reporting. This takes about 30 seconds. This only needs done once, or if the `serverless.yml` (aka SLS file) is changed. 
```bash
 sls deploy -v  # deploy with verbose reporting
 ```
\
&nbsp;

#### **Deploy Lambda Only**
To only deploy the lambda after making lambda code changes, use this command:
```bash
sls deploy --function theSLSFunctionName   # deploy/update only the lambda function
```
The `sls deploy --function` is very quick, 1-3 seconds. 
\
&nbsp;
\
&nbsp;

Remove your lambda from AWS if you manually deploy it:
```bash
sls remove -v 
```
\
&nbsp;
\
&nbsp;
#### **Note On SLS Function Name** 
  The SLS function name is found in the `serverless.yml` file below the `functions` header. 
  
  For this `stockRepo`, the SLS refers to the lambda function name as `theSLSFunctionName` 
```yml
functions:
  theSLSFunctionName:   #<--- SLS function name
    name: ${sel.......  # <---not the SLS name
```

SLS internally refers to your Lambda by the above name. `IT IS NOT YOUR LAMBDA HANDLER NAME`.
\
&nbsp;

Once deployed on AWS, you can run any AWS tests in the `AWS Console`, see CloudLogs for errors, and use all the AWS tools. You can also use Postman or any other tool as your function is live.  
\
&nbsp;

-----------------

## Fourth Steps - Deployment via the Gitlab CI/CD
Once your lambda is finished, it is time have the pipeline run. 

When you `git push` on `/feature/coolNewThing` branch, the pipeline does not run; this is intentional. The feature branch is your pure sandbox and storage of code. `/feature` requires you to `sls deploy`. 

The `dev` branch and higher automatically deploy. 
\
&nbsp;
### Steps to Merge to Dev
1) When you finish with a lambda feature branch, locally merge `/feature` changes to `dev`. 
\
&nbsp;
2) Once local `dev` branch is current, rename `gitlab-ci.XXX` file to `gitlab-ci.yml`. This file controls the pipeline.
\
&nbsp;
3) Now `push` the updated local `dev` changes to `remote` dev branch and watch the CI/CD magic run. Gitlab CI/CD is setup to automatically deploy the lambda to AWS and run other scripts needed in the `gitlab-ci.yml`. 
\
&nbsp;

`Note:`
The Gitlab pipeline process takes 2-3 minutes since various packages need installed by Gitlab. Gitlab will show you a red X or green check if the pipeline fails or succeeds. 

Don't rely on the Gitlab CI/CD process for development; it won't give you the speed you want. Use `sls deploy --function` or `ssl invoke local`!
\
&nbsp;
_______

## Testing

### Postman 
SLS creates the API Gateway (or other triggers) and when you `sls deploy` or `sls deploy --function functionName`. 

When finished deploying, SLS shows an endpoint in the CLI. As of today (6/14/21) this endpoint doesn't include the `rootResource` (for example, `/v1/`) and the endpoint shown thusly does not work. 

**Use the end point from API Gateway instead.** 

#### Feature Tests

### Test Data  

\
&nbsp;
_______
## Additional information

