## Migrate Tapatalk images to your own web server (PHPBB)

When you, as a forum owner, decide to quit Tapatalk, you might run into this problem. Many of your users may have uploaded images to Tapatalk instead of the forum, making the forum content dependent of Tapatalk.
This is undesirable, because the images will eventually get lost, when Tapatalk decides to delete them.

This script can help you migrate the images to your server. In my example the forum is a fairly big PHPBB forum with thousands of pictures hosted on Tapatalk.

My steps (for PHPBB):
* Export the posts of your forum. On PHPBB you can export all forum posts or make a selection using:  
`mysql -u <DBUSER> -p -D <DBNAME> -e "select post_text from phpbb_posts where post_text like '%https://uploads.tapatalk-cdn.com/%'" > tapatalkposts.input`  
We only use this file to extract URLs and download 
files. Above example is for MySQL.

* Run the tapatalk.py script

* Process the files according to your forum image size/quality rules. 
You can do this super easy with ImageMagick:
`find ./downloads/. -name "*.jpg" -type 'f' -exec convert '{}' -resize 860\> -quality 85 '{}' \;`

* Put the files including their directory structure somewhere on your webserver. e.g. `/static/tapatalkexport` (Or something you like)

* Replace `https://uploads.tapatalk-cdn.com` with `https://<FORUMURL>/static/tapatalkexport`  
On MySQL you can do that this way:  
`update phpbb_posts set post_text = replace(post_text, 'https://uploads.tapatalk-cdn.com', 'https://<FORUMURL>/static/tapatalkexport') where post_text like '%https://uploads.tapatalk-cdn.com%';`


#### Some notes:

The scripts looks up all matches of whole_url_regex and puts them in URLs. All URLs are downloaded and the directory structure is retained. In case of a 404 a log entry is written to `tapatalk.log`. You can handle them separately on your forum. Those images are gone on Tapatalk and not visible on your forum even before this migration.

To keep the logic of the script simple and load on the Tapatalk CDN low, the scripts puts the result, even when a 404 occurs in the files on the filesystem. Those files have a size of 30 bytes (JSON error) at the moment of writing. Way smaller than the smallest JPEG.

You can delete them easily using:
`find ./downloads/. -name "*.jpg" -type 'f' -size -30 -delete`

Use everything in this repo at your own risk.