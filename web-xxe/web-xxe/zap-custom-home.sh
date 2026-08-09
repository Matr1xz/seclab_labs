#!/usr/bin/env bash
#
# OWASP ZAP launcher with a relocatable ZAP home directory.
# Default: /tmp/$USER/.ZAP
# Override for a persistent or larger disk, for example:
#   ZAP_HOME=/mnt/storage/zap-home ./zap-custom-home.sh
#

# Dereference from link to the real directory
SCRIPTNAME="$0"

# While name of this script is symbolic link
while [ -L "${SCRIPTNAME}" ]; do
  cd "$(dirname "${SCRIPTNAME}")" > /dev/null || exit 1
  SCRIPTNAME="$(readlink "$(basename "${SCRIPTNAME}")")"
done
cd "$(dirname "${SCRIPTNAME}")" > /dev/null || exit 1

# Base directory where ZAP is installed
BASEDIR="$(pwd -P)"

# ZAP stores sessions, logs, configuration, and add-ons under this directory.
# Use ZAP_HOME=/some/other/path when starting this launcher to override it.
ZAP_HOME="${ZAP_HOME:-/tmp/${USER}/.ZAP}"
mkdir -p "$ZAP_HOME" || {
  echo "Cannot create ZAP_HOME: $ZAP_HOME" >&2
  exit 1
}

# Switch to the directory where ZAP is installed
cd "$BASEDIR" || exit 1

# Get Operating System
OS=$(uname -s)

# If we're on OS X, try to use the bundled Java; if it's not there, use system Java.
if [ "$OS" = "Darwin" ]; then
  if [ -e ../PlugIns/jre*/Contents/Home/bin/java ]; then
    pushd ../PlugIns/jre*/Contents/Home/bin > /dev/null || exit 1
    JAVA_PATH=$(pwd -P)
    PATH="$JAVA_PATH:$PATH"
    popd > /dev/null || exit 1
  fi
fi

# Extract and check the Java version
JAVA_OUTPUT=$(java -version 2>&1)

# Catch warning: Unable to find a $JAVA_HOME at "/usr", continuing with system-provided Java
if echo "$JAVA_OUTPUT" | grep -q "continuing with system-provided Java"; then
  echo "WARNING, \$JAVA_HOME could be set incorrectly, Java's error is:"
  echo "    $JAVA_OUTPUT"
  echo "Unsetting JAVA_HOME and continuing with ZAP start-up"
  unset JAVA_HOME
fi

DEFAULTJAVAGC="-XX:+UseG1GC"

JAVA_VERSION=$(java -version 2>&1 | awk -F\" '/version/ { print $2 }')
JAVA_MAJOR_VERSION=${JAVA_VERSION%%[.|-]*}
JAVA_MINOR_VERSION=$(echo "$JAVA_VERSION" | awk -F. '{ print $2 }')

# JEP 223: Java >= 9 no longer uses 1 as the major version.
if [ "$JAVA_MAJOR_VERSION" -ge 9 ]; then
  DEFAULTJAVAGC=""
  echo "Found Java version $JAVA_VERSION"
elif [ "$JAVA_MAJOR_VERSION" -ge 1 ] && [ "$JAVA_MINOR_VERSION" -ge 8 ]; then
  echo "Found Java version $JAVA_VERSION"
else
  echo "Exiting: ZAP requires a minimum of Java 8 to run, found $JAVA_VERSION"
  exit 1
fi

# Keep custom JVM options with the relocated ZAP home as well.
JVMPROPS="$ZAP_HOME/.ZAP_JVM.properties"

# Work out best memory options
if [ -f "$JVMPROPS" ]; then
  JMEM=$(head -1 "$JVMPROPS")
elif [ "$OS" = "Linux" ]; then
  MEM=$(expr "$(sed -n 's/MemTotal:[ ]\{1,\}\([0-9]\{1,\}\) kB/\1/p' /proc/meminfo)" / 1024)
elif [ "$OS" = "Darwin" ]; then
  MEM=$(system_profiler SPMemoryDataType | sed -n -e 's/.*Size: \\([0-9]\\{1,\\}\\) GB/\\1/p' | awk '{s+=$0} END {print s*1024}')
elif [ "$OS" = "SunOS" ]; then
  MEM=$(/usr/sbin/prtconf | awk '/Memory/{print $3}')
elif [ "$OS" = "FreeBSD" ]; then
  MEM=$(($(sysctl -n hw.physmem) / 1024 / 1024))
fi

if [ -n "$JMEM" ]; then
  echo "Read custom JVM args from $JVMPROPS"
  JAVAGC=""
elif [ -z "$MEM" ]; then
  echo "Failed to obtain current memory, using JVM default memory settings"
  JAVAGC=${DEFAULTJAVAGC}
else
  echo "Available memory: $MEM MB"
  JAVAGC=${DEFAULTJAVAGC}
  if [ "$MEM" -gt 512 ]; then
    QMEM=$((MEM / 4))
    JMEM="-Xmx${QMEM}m"
  fi
fi

ARGS=()
for var in "$@"; do
  if [[ "$var" == -Xmx* ]]; then
    JMEM="$var"
  elif [[ "$var" == --jvmdebug* ]]; then
    JAVADEBUGPORT=$(echo "$var" | sed -e 's/--jvmdebug//g' -e 's/=//g')
    if [ -z "$JAVADEBUGPORT" ]; then
      JAVADEBUGPORT=1044
    fi
    JAVADEBUG="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=127.0.0.1:$JAVADEBUGPORT"
  elif [[ "$var" != -psn_* ]]; then
    ARGS+=("$var")
  fi
done

if [ -n "$JMEM" ]; then
  echo "Using JVM args: $JMEM"
fi

if [ -n "$JAVADEBUG" ]; then
  echo "Setting debug: $JAVADEBUG"
fi

# Start ZAP.  The -dir option directs its .ZAP home, including sessions.
if [ "$OS" = "Darwin" ]; then
  exec java ${JMEM} ${JAVAGC} -Xdock:icon="../Resources/ZAP.icns" \
    -jar "${BASEDIR}/zap-2.9.0.jar" -dir "$ZAP_HOME" "${ARGS[@]}"
else
  exec java ${JMEM} ${JAVAGC} ${JAVADEBUG} \
    -jar "${BASEDIR}/zap-2.9.0.jar" -dir "$ZAP_HOME" "${ARGS[@]}"
fi
