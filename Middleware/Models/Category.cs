using LanguageExt;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Middleware.Models
{

    public enum GameEngine
    {
        Unity,
        Unreal,
        Random
    }

    public enum CompatiblePlatform
    {
        Windows,
        Linux,
        MacOS,
        Android,
        IOS,
        Web
    }

    public enum CompatibleLanguages
    {
        CSharp,
        Js,
        Cpp
    }

    [PrimaryKey(nameof(Id))]
    public class Category
    {
        internal Guid Id { get; set; } = default;

        public GameEngine Engine;
        public IEnumerable<CompatibleLanguages> ProgrammingLanguages;
        public IEnumerable<CompatiblePlatform> Platforms;

        internal IEnumerable<string> GetFilterable()
        {
            var result = new List<string>(ProgrammingLanguages.Count() + Platforms.Count() + 1);

            result.Add(Engine.ToString());
            result.AddRange(ProgrammingLanguages.Select(pl => pl.ToString()));
            result.AddRange(Platforms.Select(p => p.ToString()));

            return result;
        }
    }
}
