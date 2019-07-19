

# sysctl cs.sensorid


Facter.add('crowdstrike_aid') do
  setcode do
    Facter::Core::Execution.execute('/usr/sbin/sysctl -n cs.sensorid 2> /dev/null || echo NONE ')
  end
end


