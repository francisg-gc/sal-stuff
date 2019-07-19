# mac_admin_users.rb

Facter.add(:mac_chrome_extensions) do
  confine kernel: 'Darwin'
  raw_exts=Facter::Core::Execution.execute('/usr/bin/find /Users/*/Library/Application\ Support/Google/Chrome/*/Extensions -name manifest.json', {:on_fail => nil})
  setcode do
    mac_chrome_extensions=raw_exts.split("\n")
  end
end
