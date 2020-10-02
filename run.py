from get_apk_package_names import Getlists

getlist = Getlists()
getlist.init_request('basic','test','ko')
#getlist.parse_pkgnames()
apk_lists = getlist.show_apk_list()
print(len(apk_lists))
getlist.get_pkginfo()

#getlist.get_result()

