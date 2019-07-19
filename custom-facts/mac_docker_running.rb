# mac_admin_users.rb

Facter.add(:mac_docker_running) do
  confine kernel: 'Darwin'
  require 'json'
  conts=[]
  Facter::Core::Execution.execute("docker container ls  --format '{{json .}}'", {:on_fail => nil}).each_line do |line|
    conts.push(JSON.parse(line))
  end
  setcode do
    conts
  end
end
