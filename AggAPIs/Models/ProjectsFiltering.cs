using Microsoft.Build.Framework;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Middleware.Models;
using System;

namespace AggAPIs.Models
{
    public class ProjectsFiltering
    {
        public IEnumerable<GameEngine> Engines { get; set; }
        public IEnumerable<CompatiblePlatform> SupportedPlatforms { get; set; }
        public IEnumerable<CompatibleLanguages> ProgrammingLanguages { get; set; }

        public IEnumerable<Predicate<string>> GetFilter()
        {
            var filter = delegate (string a, string b) { return a.ToLower().Equals(b); };

            var result = new List<Predicate<string>>();

            result.AddRange(
                Engines.Select(e => new Predicate<string>((string c) => filter(e.ToString(), c))).ToList()
                );

            result.AddRange(
                SupportedPlatforms.Select(e => new Predicate<string>((string c) => filter(e.ToString(), c)))
                );

            result.AddRange(
                 ProgrammingLanguages.Select(e => new Predicate<string>((string c) => filter(e.ToString(), c)))
                );

            return result;
        }

    }



}
