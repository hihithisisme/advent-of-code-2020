package cmd

import (
	"aoc/src/day10"
	"aoc/src/day11"
	"aoc/src/day12"
	"aoc/src/day13"
	"aoc/src/day14"
	"aoc/src/day7"
	"aoc/src/day8"
	"aoc/src/day9"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "aoc",
	Short: "Central command for all AoC challenges",
	Long:  `Use the number that corresponds to the day of the challenge to run`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	//Run: func(cmd *cobra.Command, args []string) {},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	cobra.CheckErr(rootCmd.Execute())
}

func init() {
	rootCmd.AddCommand(
		day7.Cmd,
		day8.Cmd,
		day9.Cmd,
		day10.Cmd,
		day11.Cmd,
		day12.Cmd,
		day13.Cmd,
		day14.Cmd,
	)
	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.

	//rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.aoc.yaml)")

	// Cobra also supports local flags, which will only run
	// when this action is called directly.
	//rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
