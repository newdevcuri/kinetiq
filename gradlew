#!/bin/sh

# Gradle start up script for POSIX generated for Nocturne Android project

JAVACMD="java"
which java >/dev/null 2>&1 || {
    echo "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH." >&2
    exit 1
}

# Resolve Gradle Jar
DIRNAME="$(dirname "$0")"
[ -z "$DIRNAME" ] && DIRNAME="."
APP_BASE_NAME="$(basename "$0")"
APP_HOME="$(cd "$DIRNAME" && pwd)"

CLASSPATH="$APP_HOME/gradle/wrapper/gradle-wrapper.jar"

# If gradle wrapper jar does not exist, download or run gradle directly
if [ ! -f "$CLASSPATH" ]; then
    mkdir -p "$APP_HOME/gradle/wrapper"
    if which gradle >/dev/null 2>&1; then
        exec gradle "$@"
    fi
    echo "Downloading Gradle Wrapper..."
    curl -sLo "$CLASSPATH" https://raw.githubusercontent.com/gradle/gradle/v8.7.0/gradle/wrapper/gradle-wrapper.jar || true
fi

if [ -f "$CLASSPATH" ]; then
    exec "$JAVACMD" "-Dorg.gradle.appname=$APP_BASE_NAME" -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
elif which gradle >/dev/null 2>&1; then
    exec gradle "$@"
else
    echo "ERROR: Gradle or Gradle Wrapper JAR not found. Please install gradle or run on GitHub Actions." >&2
    exit 1
fi
