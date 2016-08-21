import sys

_meta_shell_command = 'template_cs'

template = """
//Compile: `mono-csc code.cs`.

using System;
using System.Linq;
using System.Collections.Generic;

public class Solution
{
	static public void Main (string[] args)
	{
		Console.WriteLine ("Start");
	}
}
"""

if __name__ == '__main__':
    name = 'code.cs'

    if len(sys.argv) > 1:
        name = sys.argv[1]

    open(name, 'w').write(template)
