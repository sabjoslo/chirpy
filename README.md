![](http://cs.mcgill.ca/~hsalee/images/chipy.png)


# *chirpy* 
a command line interface for quickly collecting and parsing Twitter data.

***

chirpy is a command line tool for swift and streamlined collection of Twitter data. The toolset is capable of collecting already posted tweets, actively tracking the live Twitter feed for specific keywords and retrieving user history along with additional resources for parsing captured data.

There are three tools for data collection - `search`, `stream`, `user` and two for parsing `tophash` and `parse`. Additional tools involve handling Twitter API profiles and managing running streams.

***

## Installation

The easiest way to install the latest version is by using pip/easy_install to pull it from PyPI:

    pip install chirpy

You may also use Git to clone the repository from Github and install it manually:

    git clone https://github.com/elric-dev/chirpy
    cd chirpy
    python setup.py install
    pip install -r requirements.txt

Note that this installs the original version of chirpy, and not the current fork, which is still under development.
***

## Configuration

On installation, chirpy creates a directory `.chirpy` in user home. The directory houses the file `chirpy.config` that saves the paths for log files and profile files. By default, they are stored in `.chirpy/logs` and `.chirpy/profiles` respectively. A root path can also be specified to save the captured files in a particular directory.

***

## Synopsis

	chirpy [options] flags

***


## Data collection options

- `search`: search Twitter for a partcular keyword.
- `stream`: actively track a live Twitter stream for a particular keyword.
- `user`: retrive atmost the recent 3200 tweets form a users's timeline.

## Data parsing options

- `tophash`: list the tophashtags in a captured file.
- `parse`: convert a txt file of json objects to a csv file.

## Stream management options 

- `stream_list`: lists the current runnign stream trackers.
- `stream_remove`: remove an existing stream.

## Profile management options 

- `profile_add`: adds a new Twitter API auth profile.
- `profile_list`: lists all added Twitter API auth profiles.
- `profile_remove`: removes an existing Twitter API auth profile.

***

## Managing profiles

Before you can start using the APIs, you would need API keys. The API keys include consumer key, consumer secret and access token, access secret.  

Since the API keys are rate-limited, a single profile is not used for concurrent tasks. For running multiple tasks at once, more than one profile is required.

It has three available options: profile_add, profile_list and profile_remove.


#### ADD:


	chirpy profile_add



You will be prompted to enter the:

a. Twitter username
b. Consumer_key
c. Consumer_secret
d. Access_token
e. Access_token_secret

A profile is then added in the profile path under the username.

#### LIST:


	chirpy profile_list


You are provided with the lists of all the current profiles and their status : Free / In Use.

#### REMOVE:
	
	chirpy profile_remove

You will be prompted to enter the username.
Be sure to type the profile name properly so not to delete the wrong profile.
You will then be prompted to confirm deleting the profile. Type y.

***

## The search option

Search looks for already published tweets containg a keyword. While not mentioned officailly, the API can only retrieve tweets 7-10 days old. The crawler saves the json objects of the tweets in a txt file, one per line.

#### Usage

	chirpy search –k \#hashtag –o output_dir –f output_file -n num

- **-k**: keyword for search. `\` is to user the `#` symbol, not required if `#` not used.
- **-o**: *output_dir* is created in `pwd` if not present, for storing the captured file. `dpath` can be mentioned in `harvest.config` to specify a root path for storing all data. The directory would be created there in that case. 
- **-f**: *output_file* is saved in **/output_dir/**.
- **-n**: optional flag to limit the number of tweets you want to save.

Example: `chirpy search -k hello -o testhello -f hello.txt -n 800`

This will search for tweets with **hello**, list them in a txt file named **hello.txt** and place them in a directory named **testhello** inside the current directory. Since n = 800 is specified, the crawler stops after 800 tweets are collected.

```
user:~$ chirpy search -k hello -o testhello -f hello.txt -n 800
Getting Configurations
Output Directory Created
Configuring Files
Encoding Query
Retrieving Twitter Profile
Authorizing Twitter Profile
Starting Search
Tweets Collected:  100
Tweets Collected:  200
Tweets Collected:  300
Tweets Collected:  400
Tweets Collected:  500
Tweets Collected:  600
Tweets Collected:  700
Tweets Collected:  800
Deadline Reached 
Exiting
Writing To File
```

***

## Getting user history 

The option `user` can be used to access tweets from a particular user or a list of users. Twitter allows access to only the last 3200 tweets. The crawler saves the json objects of the tweets in a separate txt file for each user, one per line. The option would only work if the account(s) are public.

The results are saved in user_name.txt in the approproate directories.

#### Usage

	chirpy user [user_name ...] [options]

- **-u**: username of the Twitter follower(s). Can be user's screen name or user ID. @ is not required.

**Options**
- **-i**: Input file. If specified, the list of users is extracted line-by-line from *input_file*.
- **-u**: username of the Twitter follower(s). Can be user's screen name or user ID. @ is not required.
- **-f**: Output file. If specified, the crawler saves the json objects of the tweets in *output_file* in pwd.
- **-o**: Output directory. If specified, the crawler saves the json objects of the tweets in a separate txt file for each user in *output_dir*, one per line. *output_dir* is created in `pwd` if not present, for storing the captured file. `dpath` can be mentioned in `chirpy.config` to specify a root path for storing all data. The directory would be created there in that case.
**Note:** If both *output_file* and *output_dir* are specified, *output_dir* is ignored and *output_file* is created in pwd. If neither are specified, json objects of the tweets are written to stdout.
- **-n**: *num_tweets* specifies the number of (most recent) tweets to be collected. If unspecificed, *num_tweets* defaults to 3,200.
- **--retweets** includes retweets in output. If unspecified, retweets are not included in output. **Note:** Twitter includes retweets in rate limits whether --retweets flag is included or not. If *num_tweets* is specified and is below rate limit, retweets will **not** be included in collection count.
- **--overwrite**: If it exists, overwrite user_name.txt in output_dir file with current output.

The option creates username.txt in output_dir to save the results.

Example: `chirpy user -u saleemq90 -o testhello`

This will search for tweets by user **saleemq90**, list them in a txt file named **saleemq90.txt**, and place them in a directory named **testhello** inside the current directory. 

```
user:~$ chirpy user -u saleemq90 -o testhello
Accessing User saleemq90
Getting Configurations
Configuring Files
Retrieving Twitter Profile
Authorizing Twitter Profile
Extracting User Tweets
Tweets Collected:  57
Writing To File
```

***

## The stream option

Stream actively listens to an active Twitter stream looking for tweets containg a keyword. The tarcker saves the json objects of the tweets in a txt file, one per line. Once the tracker is setup, it runs in the background for specified number of days and then terminates.

#### Usage

        chirpy stream –k \#hashtag –o output_dir –f output_file -d days

- **-k**: keyword for search. `\` is to user the `#` symbol, not required if `#` not used.
- **-o**: *output_dir* is created in `pwd` if not present, for storing the captured file. `dpath` can be mentioned in `harvest.config` to specify a root path for storing all data. The directory would be created there in that case. 
- **-f**: *output_file* is saved in **/output_dir/**.
- **-d**: set the number of days the tracker runs before terminating.

Example: `chirpy stream -k hello -o testhello -f hello.txt -d 3`

This will setup a tracker for tweets with **hello**, list them in a txt file named **hello.txt** and place them in a directory named **testhello** inside the current directory. Since d = 3, the tracker terminates after 3 days.

```
user:~$ chirpy stream -k hello -o testhello -f hello.txt -d 3
Stream Started
```

### Managing streams

#### List streams

	chirpy stream_list

Lists all the currently running streams.


```
(trusty)ndg01@carpathia:~$ twitterstream list
runnign streams...
+------+--------------+------------------+----------+--------------+
| Pid  | Query        | Tweets Collected | Run time | Profile      |
+------+--------------+------------------+----------+--------------+
| 3517 | #walterscott | 9657             | 6:09:54  | KellyPDillon |
|      |              |                  |          |              |
+------+--------------+------------------+----------+--------------+
```

#### Remove streams

	chirpy stream_remove –p pid

* **-p**: process id of the stream you want to terminate.

Example: `twitterstream remove –p 3517`

This will remove the stream with id 3517, obtained from list.

***

## Parsing saved data

#### Viewing top hashtags in a file

	chirpy tophash –i inputfile –n top_n

* **-i**: input file.
* **-n**: look for top n hashtags. (Optional, defaults to top 100)

Example: `chirpy tophash –i pence.txt –n 10`

This will look for top 10 hashtags in **pence.txt**.

```
user:~$ chirpy tophash -i waltersearch.txt -n 10
+------------------+-----------+
| Hashtag          | Frequency |
+------------------+-----------+
| walterscott      |    365148 |
| blacklivesmatter |     20502 |
| mikebrown        |      8340 |
| michaelslager    |      7220 |
| ferguson         |      5177 |
| ericgarner       |      4739 |
| trayvonmartin    |      2955 |
| chsnews          |      2880 |
| feidinsantana    |      2091 |
| southcarolina    |      2087 |
+------------------+-----------+
```


***

#### Converting to CSV

The parse option converts a json text file into csv.

	chirpy parse –i inputfile –f out_file 


* **-i**: input file for the analysis.
* **-f**: out_file would be created in the current folder.

Example: `chirpy parse -i pence.txt –f pence.csv`

This will create a csv file of the input file.

**Note**: If output name is not given, a default name is selected, which is the inputname+_csvfile.csv.

##### Additional options

To restrict the csv to a keyword:
	
	chirpy parse –i inputfile –f out_file –k keyword

* **-k**: The csv file would only have results with the keyword

To restrict the csv to a particular user:
	
	chirpy parse –i inputfile –f out_file –u user

* **-u**: The csv file would only have tweets from the user with the specific username.

**Note**: These options can be used together.

