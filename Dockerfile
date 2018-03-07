FROM tomcat:latest
MAINTAINER v1.0
#delete old war package
#RUN rm -rf /usr/local/tomcat/webappsxxx.war
ADD sample.war /usr/local/tomcat/webapps
