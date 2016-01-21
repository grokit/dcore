import sys

_meta_shell_command = 'template_cs'

template = """
//Compile: `mono-csc code.cs`.

using System;
using System.Linq;
using System.Collections.Generic;

public class HelloWorld
{
	static public void Main ()
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
