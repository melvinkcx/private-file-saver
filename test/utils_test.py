from core.utils import calc_md5sum


def test_calc_md5sum(tmpdir):
    tmp_file = tmpdir.join("test.txt")
    tmp_file.write("xxxxxxxxxx")
    assert calc_md5sum(tmp_file) == '336311a016184326ddbdd61edd4eeb52', "calc_md5sum calculation mismatched"
