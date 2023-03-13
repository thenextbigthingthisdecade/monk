use clap::Parser;
use colored::*;
use nom::branch::alt;
use nom::bytes::complete::tag;
use nom::character::complete::{alpha1, alphanumeric1};
use nom::combinator::recognize;
use nom::multi::many0_count;
use nom::sequence::pair;
use nom::IResult;
use rustyline::error::ReadlineError;
use rustyline::{DefaultEditor, Result};
use std::fs;

#[derive(Parser)]
#[clap(author = "Prakhar Nagpal", version, about = "A very simple compiler")]
struct Args {
    #[clap(short, long, value_parser)]
    file: Option<String>,
}

fn run_compiler(file: String) -> Result<()> {
    println!(
        "{} {} {}",
        format!("Welcome to"),
        format!("Monk(s)").green().bold(),
        format!("interpreter. A simple programming language")
    );
    println!("Compiling file: {}", file);
    let contents = fs::read_to_string(&file)
        .expect("Ensure that the file is present, and has the correct file format.");
    run(&contents)
}

fn run_interpreter() -> Result<()> {
    println!(
        "{} {} {}",
        format!("Welcome to"),
        format!("Monk(s)").green().bold(),
        format!("interpreter. A simple programming language")
    );
    let mut rl = DefaultEditor::new()?;
    if rl.load_history("interpreter_hist.txt").is_err() {
        println!("No previous history.");
    }
    loop {
        let readline = rl.readline("|> ");
        match readline {
            Ok(line) => {
                rl.add_history_entry(line.as_str());
                run(line.trim()).unwrap();
            }
            Err(ReadlineError::Interrupted) => {
                println!("{}", format!("Session interrupted [SIGINT].").red());
                break;
            }
            Err(ReadlineError::Eof) => {
                println!("Exiting Monk!");
                break;
            }
            Err(err) => {
                println!("Error: {:?}", err);
                break;
            }
        }
    }
    rl.save_history("interpreter_hist.txt")
}

fn parse(input: &str) -> IResult<&str, &str> {
    recognize(pair(
        alt((alpha1, tag("_"))),
        many0_count(alt((alphanumeric1, tag("_")))),
    ))(input)
}

fn run(input: &str) -> Result<()> {
    let res = parse(&input);
    println!("value of parse: {}", res);
    Ok(())
}

fn main() -> Result<()> {
    let args = Args::parse();
    match args.file {
        None => run_interpreter(),
        Some(f) => run_compiler(f),
    }
}
