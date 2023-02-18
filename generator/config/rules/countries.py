# coding: utf-8

COUNTRIES: dict = {
    "FRANCE": {
        "COUNTRY_CODE": "33",
        "OPERATOR_CODES": {
            "MOBILE": [
                "699", "698", "695", "68", "67", "6699", "6698", "669", "668", "666", "667", "665", "663",
                "664", "660", "661", "662", "659", "658", "6567", "6568", "6449", "6448", "6447", "6440",
                "6419", "6418", "6415", "6414", "6413", "6412", "6411", "6410", "65666", "65667", "65668",
                "65669", "655", "654", "6535", "6536", "6537", "6538", "6539", "6530", "6531", "6532", "6533",
                "6534", "652", "651", "650", "64999", "64995", "64998", "64992", "64993", "64990", "64991",
                "6496", "6497", "6498", "64951", "64952", "64953", "64954", "64955", "64956", "64957", "64958",
                "64959", "6490", "6491", "6492", "6493", "6494", "648", "647", "646", "645",
                "6444", "6445", "6446", "6441", "6442", "6443", "643", "642",
                "6417", "64166", "64167", "64168", "64169", "64164", "64160", "64161",
                "6401", "6402", "6403", "6404", "6405", "6406", "6407", "6408", "6409",
                "64005", "64006", "64007", "64008", "64009", "6381", "6382", "6383", "6384", "6385", "6386",
                "6387", "6388", "6389", "63801", "63802", "63803", "63804", "63805", "637", "6365", "6366",
                "6367", "6368", "6369", "6360", "6361", "6362", "6363", "6364", "635", "634", "633", "632",
                "631", "630", "62", "61",
                "7"
            ],
            "DESK": ["1", "2", "3", "4", "5"]
        },

        "FINE_TUNING": {
            # * ... Number of digits in the complete phone suffix, operator code included
            "NDIGITS": 9,
            # * ... Maximum same digit amount in the generated block
            "SAME_DIGIT_THRESHOLD": 5,
            # * ... Maximum consecutive same digit amount anywhere in the generated block
            "CONSECUTIVE_SAME_DIGIT_THRESHOLD": 5,
            # * ... Maximum consecutive 0 amount in the beginning of the generated block
            "HEAD_MAX_ZEROS": 1
        }
    }
}
