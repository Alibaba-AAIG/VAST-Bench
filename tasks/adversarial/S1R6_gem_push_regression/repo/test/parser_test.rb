require_relative "test_helper"
require "acme/parser"

class ParserSizeTest < Minitest::Test
  def test_plain_bytes
    assert_equal 512, Acme::Parser.parse_size("512")
    assert_equal 512, Acme::Parser.parse_size("512B")
  end

  # Regression guard: the edge config loader and the upload gate both treat a
  # "KB" as a binary kibibyte (1024 bytes). A 16KB upload cap must be 16384.
  def test_kb_is_binary
    assert_equal 1024, Acme::Parser.parse_size("1KB")
    assert_equal 16384, Acme::Parser.parse_size("16KB")
  end

  # MB / GB / TB follow the same binary ladder used by the storage accounting.
  def test_mb_gb_tb_are_binary
    assert_equal 1024**2, Acme::Parser.parse_size("1MB")
    assert_equal 2 * 1024**3, Acme::Parser.parse_size("2GB")
    assert_equal 1024**4, Acme::Parser.parse_size("1TB")
  end

  def test_rejects_unknown_unit
    assert_raises(ArgumentError) { Acme::Parser.parse_size("5PB") }
    assert_raises(ArgumentError) { Acme::Parser.parse_size("not a size") }
  end
end
