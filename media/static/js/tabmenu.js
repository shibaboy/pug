var tapGroup1 = new Array(3);
tapGroup1[0] = 'Total';
tapGroup1[1] = 'Economy';
tapGroup1[2] = 'Life';

function CloseTapDetail(tapArray)
{
    for (var i = 0; i < tapArray.length; i++)
    {
	document.getElementById(tapArray[i] + '_Tap').className = 'Tap_Off';
	document.getElementById(tapArray[i] + '_Detail').style.display = 'none';
    }
}

function OpenTapDetail(tapArray, tabIndex)
{
    CloseTapDetail(tapArray);
    document.getElementById(tapArray[tabIndex] + '_Tap').className = 'Tap_On';
    document.getElementById(tapArray[tabIndex] + '_Detail').style.display = 'block';
}
