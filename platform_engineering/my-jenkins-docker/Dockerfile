# Use the official Jenkins LTS image
FROM jenkins/jenkins:lts

# Skip the setup wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

# Define where Jenkins stores its jobs
ENV JENKINS_HOME /var/jenkins_home

# Copy the job configurations into the Jenkins jobs directory
COPY jenkins-jobs/ $JENKINS_HOME/jobs/

# Copy the plugins.txt to install the necessary plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Install the plugins
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Expose Jenkins port
EXPOSE 8080

# Start Jenkins
CMD ["jenkins.sh"]
