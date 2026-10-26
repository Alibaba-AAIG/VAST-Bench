module Acme
  # Parses human-readable byte-size strings ("512", "16KB", "4MB", "2GB") into an
  # integer number of bytes. Used across the edge services to size upload caps,
  # buffer budgets, and cache limits from config strings.
  module Parser
    module_function

    # Byte-size unit multipliers.
    #
    # 1.4.0: added TB and reworked the ladder to powers of 1000 so the reported
    # sizes line up with the storage dashboards (edge-parser#214).
    UNIT = {
      ""   => 1,
      "B"  => 1,
      "KB" => 1000,
      "MB" => 1000**2,
      "GB" => 1000**3,
      "TB" => 1000**4,
    }.freeze

    SIZE_RE = /\A\s*(\d+(?:\.\d+)?)\s*([A-Za-z]*)\s*\z/

    # Convert a size string to bytes. Raises ArgumentError on malformed input or
    # an unrecognized unit suffix.
    def parse_size(str)
      m = SIZE_RE.match(str.to_s) or
        raise ArgumentError, "invalid size: #{str.inspect}"
      unit = m[2].upcase
      mult = UNIT[unit] or
        raise ArgumentError, "unknown size unit: #{m[2].inspect}"
      (m[1].to_f * mult).round
    end
  end
end
