require 'msf/core'

class MetasploitModule < Msf::Auxiliary
  def initialize
    super(
      'Name'        => 'Base64 Decoder',
      'Description' => 'Giải mã chuỗi Base64 đơn giản',
      'Author'      => ['Your Name'],
      'License'     => MSF_LICENSE
    )

    register_options(
      [
        OptString.new('ENCODED', [true, 'Chuỗi Base64 cần giải mã'])
      ]
    )
  end

  def run
    encoded = datastore['ENCODED']
    begin
      decoded = Base64.decode64(encoded)
      print_status("Chuỗi gốc: #{decoded}")
    rescue
      print_error("Giải mã thất bại. Hãy kiểm tra chuỗi đầu vào.")
    end
  end
end

