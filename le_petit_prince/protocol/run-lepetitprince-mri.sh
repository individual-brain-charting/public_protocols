#! /bin/bash
# Time-stamp: <2019-03-12 17:19:52 christophe@pallier.org>

tempfile=`(tempfile) 2>/dev/null` || tempfile=/tmp/test$$
trap "rm -f $tempfile" 0 $SIG_NONE $SIG_HUP $SIG_INT $SIG_QUIT $SIG_TERM

QUEST=questions_a_presenter.pdf

resp=0

until [ "$resp" = "Quit" ]
do
    next=$(($resp + 1))
    if [ $next = "11" ]; then
        next="Quit";
    fi

    dialog --clear --title "Le Petit Prince" "$@" \
         --nocancel --default-item  "$next" \
         --menu "Please select the run number and press Enter\n" \
             24 40 11 \
             1 "Chapters 1-3" \
             2 "Chapters 4-5" \
             3 "Chapters 6-8" \
             4 "Chapters 9-10" \
             5 "Chapters 11-13" \
             6 "Chapters 14-17" \
             7 "Chapters 18-20" \
             8 "Chapters 21-23" \
             9 "Chapters 24-27" \
             10 "Localizer" \
             Quit  "End the experiment"  2>$tempfile

  retvat=$?
  resp=$(cat $tempfile)

  case $resp in
      1) python lepp_mri.py 'wav/ch1-3.wav'
         dialog --msgbox "evince -s -p 4  ${QUEST}" 6 32 ;;
      2) python lepp_mri.py 'wav/ch4-6.wav'
         dialog --msgbox "evince -s -p 11  ${QUEST}" 6 32 ;;
      3) python lepp_mri.py 'wav/ch7-9.wav'
         dialog --msgbox "evince -s -p 18  ${QUEST}" 6 32 ;;
      4) python lepp_mri.py 'wav/ch10-12.wav'
         dialog --msgbox "evince -s -p 25 ${QUEST}" 6 32 ;;
      5) python lepp_mri.py 'wav/ch13-14.wav'
         dialog --msgbox "evince -s -p 31 ${QUEST}" 6 32 ;;
      6) python lepp_mri.py 'wav/ch15-19.wav'
         dialog --msgbox "evince -s -p 38 ${QUEST}" 6 32 ;;
      7) python lepp_mri.py 'wav/ch20-22.wav'
         dialog --msgbox "evince -s -p 45 ${QUEST}" 6 32 ;;
      8) python lepp_mri.py 'wav/ch23-25.wav'
         dialog --msgbox "evince -s -p 52  ${QUEST}" 6 32 ;;
      9) python lepp_mri.py 'wav/ch26-27.wav'
         dialog --msgbox "evince -s -p 59  ${QUEST}" 6 32 ;;
      10) (cd ../localizer; python localizer-speech.py list.csv; cd ..) ;;
      Quit) echo "Finito!" ;;
      *) dialog --msgbox "I do not understand..." 6 32 ;;
  esac

done
