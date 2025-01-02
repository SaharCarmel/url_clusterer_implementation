import pytest
from cluster import cluster_urls

INPUT_URLS = [
    "https://www.github.com/user/abc/profile",
    "https://www.github.com/user/cba/profile",
    "https://www.github.com/user/bac/profile",
    "https://www.facebook.com/user/bac/profile",
    "http://www.facebook.com/user/ccc/profile",
    "http://www.facebook.com/user/bcc/profile",
    "http://www.github.com/user/bac/profile",
    "https://ynet-images1.yit.co.il/Common/Api/Scripts/paywall.js",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/2022/07/13/Bk6h8dhoq/Bk6h8dhoq_0_0_1300_732_0_large.jpg",
    "https://www.amazon.com/api/v1/product/3154831598/price",
    "https://www.amazon.com/api/v1/product/3154831598/details",
    "http://172.31.3.182:3101/ready",
    "http://172.39.8.180:3102/ready",
    "https://github.com/organization/project/show_partial",
    "https://profootballtalk.nbcsports.com/2022/07/20/49ers-trade/",
    "https://twitter.com/HezyLaplacian/status/1548959887159316192",
    "https://twitter.com/hasolidit/status/1549775507177183851",
    "https://twitter.com/MBlumenblat/status/1541801287934446544",
    "https://www.amazon.com/1/seller/c4f4842c-97a2-4c7a-b077-66a4b3fc6b34/details",
    "https://www.amazon.com/2/seller/c4f4842c-97a2-4c7a-b077-66a4b3fc6b34/details",
    # Additional GitHub user profile URLs
    "https://www.github.com/user/xyz123/profile",
    "https://www.github.com/user/def456/profile",
    # Additional Twitter status URLs
    "https://twitter.com/elonmusk/status/1234567890123456789",
    "https://twitter.com/BillGates/status/9876543210987654321",
    "https://twitter.com/tim_cook/status/5555555555555555555",
    # Additional Amazon product URLs
    "https://www.amazon.com/api/v1/product/9876543210/price",
    "https://www.amazon.com/api/v1/product/5555555555/details",
    # Additional Ynet images
    "https://ynet-images1.yit.co.il/Common/Api/Scripts/analytics.js",
    "https://ynet-images1.yit.co.il/Common/Api/Scripts/tracking.js",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/2023/01/15/ABC123def/ABC123def_0_0_850_550_0_large.jpg",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/2023/02/20/DEF456ghi/DEF456ghi_0_0_850_550_0_large.jpg",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/2023/03/25/GHI789jkl/GHI789jkl_0_0_850_550_0_large.jpg",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/2023/04/30/JKL012mno/JKL012mno_0_0_850_550_0_large.jpg",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/2023/05/10/MNO345pqr/MNO345pqr_0_0_850_550_0_large.jpg",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/2023/06/15/PQR678stu/PQR678stu_0_0_850_550_0_large.jpg",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/2023/07/20/STU901vwx/STU901vwx_0_0_850_550_0_large.jpg",
    # Additional seller URLs
    "https://www.amazon.com/1/seller/a1b2c3d4-e5f6-7g8h-i9j0-k1l2m3n4o5p6/details",
    "https://www.amazon.com/2/seller/98765432-abcd-efgh-ijkl-mnopqrstuvwx/details",
    # Additional NBCSports articles
    "https://profootballtalk.nbcsports.com/2023/04/15/draft-analysis-top-prospects/",
    "https://profootballtalk.nbcsports.com/2023/04/16/team-rankings-2023/"
]

EXPECTED_PATTERNS = [
    "https://www.github.com/user/*/profile",
    "https://www.facebook.com/user/*/profile",
    "https://ynet-images1.yit.co.il/Common/Api/Scripts/*.js",
    "https://ynet-images1.yit.co.il/picserver5/crop_images/*/*/*/*/*.jpg",
    "https://www.amazon.com/api/v1/product/*/price",
    "https://www.amazon.com/api/v1/product/*/details",
    "http://172.31.3.182:3101/ready",
    "http://172.39.8.180:3102/ready",
    "https://github.com/organization/project/show_partial",
    "https://profootballtalk.nbcsports.com/*/*/*/*/",
    "https://twitter.com/*/status/*",
    "https://www.amazon.com/1/seller/*/details",
    "https://www.amazon.com/2/seller/*/details"
]

def test_individual_patterns():
    # First pass to train the patterns
    cluster_urls(INPUT_URLS)
    
    # Second pass to get the actual results
    result = cluster_urls(INPUT_URLS)
    
    # Test GitHub user profile patterns
    github_patterns = [p for p in result if "github.com/user" in p]
    github_success = all(p.endswith("/*/profile") for p in github_patterns)
    print(f"\nGitHub patterns: {'✓' if github_success else '✗'} ({len(github_patterns)} found)")
    
    # Test Twitter status patterns
    twitter_patterns = [p for p in result if "twitter.com" in p]
    twitter_success = all(p.endswith("/status/*") for p in twitter_patterns)
    print(f"Twitter patterns: {'✓' if twitter_success else '✗'} ({len(twitter_patterns)} found)")
    
    # Test Amazon patterns
    amazon_patterns = [p for p in result if "amazon.com" in p]
    amazon_success = all("*" in p for p in amazon_patterns)
    print(f"Amazon patterns: {'✓' if amazon_success else '✗'} ({len(amazon_patterns)} found)")
    
    assert github_success and twitter_success and amazon_success, "Some pattern groups failed validation"
