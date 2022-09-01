using System;

namespace GraslayStart
{
	static class Program
	{
		/// <summary>
		/// アプリケーションのメイン エントリ ポイントです。
		/// </summary>
		[STAThread]
		static void Main()
		{
			string exePath = System.Reflection.Assembly.GetExecutingAssembly().Location;
			string folderPath = System.IO.Path.GetDirectoryName(exePath);
			System.IO.Directory.SetCurrentDirectory(folderPath);
			
			System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
			startInfo.FileName = "pyxel.exe";
			startInfo.Arguments = "play graslay.pyxapp";
			startInfo.CreateNoWindow = true;
			startInfo.UseShellExecute = false;
			System.Diagnostics.Process.Start(startInfo);
		}
	}
}
