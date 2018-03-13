# VCF to ICS

## About
Python Command Line script to convert birthdays from [VCF or vCard](https://en.wikipedia.org/wiki/VCard) contacts to iCalendar [ICS](https://en.wikipedia.org/wiki/ICalendar) file format.  
Generate v2.0 ICS iCalendars from vCard v2.1, v3.0 and v4.0 VCF file formats. See RFC [6350](https://tools.ietf.org/html/rfc6350) and [5545](https://tools.ietf.org/html/rfc5545).  
Tested with vCard exports from Android [Contacts](https://play.google.com/store/apps/details?id=com.google.android.contacts&hl=fr) and [MCBackup](https://play.google.com/store/apps/details?id=com.globile.mycontactbackup&hl=fr) applications.

## Usage
Run `vcf_to_ics.py` with the following command line arguments :

- `-i PATH_TO/input_vcard_file.vcf`
- `-o PATH_TO/output_icalendar_file.ics`
- `-n Calendar name`

Example : `python3 vcf_to_ics.py -i "D:\DOCS\contacts.vcf" -o "D:\DOCS\birthdays.ics" -n Birthdays`

## Requirements
- [Python 3](https://www.python.org/)
  
## License
VCF to ICS is released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html).
